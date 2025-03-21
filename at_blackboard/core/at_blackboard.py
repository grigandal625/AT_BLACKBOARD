from typing import Dict
from typing import List
from typing import Optional
from typing import TypedDict
from typing import Union

from at_queue.core.at_component import ATComponent
from at_queue.core.session import ConnectionParameters
from at_queue.utils.decorators import authorized_method


class BBItemDict(TypedDict):
    ref: str
    value: Optional[Union[str, int, float, bool]]
    belief: Optional[Union[int, float]]
    probability: Optional[Union[int, float]]
    accuracy: Optional[Union[int, float]]


class EBBItemDict(BBItemDict):
    value: Optional[Union[str, int, float, bool]]


class ATBlackBoard(ATComponent):
    _bb: Dict[str, Dict[str, BBItemDict]]

    def __init__(self, connection_parameters: ConnectionParameters, *args, **kwargs):
        super().__init__(connection_parameters, *args, **kwargs)
        self._bb = {}

    @authorized_method
    async def set_item(
        self,
        ref: str,
        value: Optional[Union[str, int, float, bool]] = None,
        belief: Optional[Union[int, float]] = None,
        probability: Optional[Union[int, float]] = None,
        accuracy: Optional[Union[int, float]] = None,
        auth_token: str = None,
        **kwargs,
    ) -> BBItemDict:
        auth_token = auth_token or "default"
        auth_token_or_user_id = await self.get_user_id_or_token(auth_token, raize_on_failed=False)
        dir_key = auth_token_or_user_id
        dir = self._bb.get(dir_key, {})

        if value is None:
            dir.pop(ref, None)
            self._bb[dir_key] = dir
            return self.empty_item

        item: BBItemDict = {}
        item["ref"] = ref
        item["value"] = value
        item["belief"] = belief
        item["probability"] = probability
        item["accuracy"] = accuracy
        item.update(kwargs)

        dir[ref] = item
        self._bb[dir_key] = dir
        return item

    @authorized_method
    async def set_items(self, items: List[BBItemDict], auth_token: str = None) -> List[BBItemDict]:
        auth_token = auth_token or "default"
        auth_token_or_user_id = await self.get_user_id_or_token(auth_token, raize_on_failed=False)
        dir_key = auth_token_or_user_id
        dir = self._bb.get(dir_key, {})

        result = []
        for item in items:
            ref = item["ref"]
            value = item["value"]
            belief = item.get("belief")
            probability = item.get("probability")
            accuracy = item.get("accuracy")

            if value is None:
                dir.pop(ref, None)
                self._bb[dir_key] = dir
                return self.empty_item

            item: BBItemDict = {}
            item["ref"] = ref
            item["value"] = value
            item["belief"] = belief
            item["probability"] = probability
            item["accuracy"] = accuracy

            dir[ref] = item
            self._bb[dir_key] = dir
            result.append(item)
        return result

    @authorized_method
    async def get_item(self, ref: str, auth_token: str = None) -> EBBItemDict:
        auth_token = auth_token or "default"
        auth_token_or_user_id = await self.get_user_id_or_token(auth_token, raize_on_failed=False)
        dir_key = auth_token_or_user_id

        dir = self._bb.get(dir_key, {})
        item = dir.get(ref)
        if item is None:
            return self.empty_item
        return item

    @authorized_method
    async def get_items(self, refs: List[str], auth_token: str = None) -> List[EBBItemDict]:
        auth_token = auth_token or "default"
        auth_token_or_user_id = await self.get_user_id_or_token(auth_token, raize_on_failed=False)
        dir_key = auth_token_or_user_id

        result = []

        for ref in refs:
            dir = self._bb.get(dir_key, {})
            item = dir.get(ref)
            if item is None:
                result.append(self.empty_item)
            result.append(item)
        return result

    @authorized_method
    async def get_all_items(self, auth_token: str = None) -> List[BBItemDict]:
        auth_token = auth_token or "default"
        auth_token_or_user_id = await self.get_user_id_or_token(auth_token, raize_on_failed=False)
        dir_key = auth_token_or_user_id
        dir = self._bb.get(dir_key, {})
        return list(dir.values())

    @authorized_method
    async def clear(self, auth_token: str = None):
        auth_token = auth_token or "default"
        auth_token_or_user_id = await self.get_user_id_or_token(auth_token, raize_on_failed=False)
        dir_key = auth_token_or_user_id

        self._bb[dir_key] = {}

        return True

    @property
    def empty_item(self):
        item: EBBItemDict = {}
        item["ref"] = None
        item["value"] = None
        item["belief"] = None
        item["probability"] = None
        item["accuracy"] = None
        return item
