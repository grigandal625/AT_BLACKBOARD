from at_queue.core.at_component import ATComponent
from at_queue.core.session import ConnectionParameters
from at_queue.utils.decorators import authorized_method
from typing import TypedDict, Dict, Optional, Union, List


class BBItemDict(TypedDict):
    ref: str
    value: Union[str, int, float, bool]
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
    def set_item(
        self, 
        ref: str,
        value: Optional[Union[str, int, float, bool]] = None,
        belief: Optional[Union[int, float]] = None,
        probability: Optional[Union[int, float]] = None,
        accuracy: Optional[Union[int, float]] = None,
        **kwargs
    ) -> BBItemDict:
        dir_key = kwargs.pop('auth_token', 'default')
        dir = self._bb.get(dir_key, {})
        
        if value is None:
            dir.pop(ref, None)
            self._bb[dir_key] = dir
            return self.empty_item

        item: BBItemDict = {}
        item['ref'] = ref
        item['value'] = value
        item['belief'] = belief
        item['probability'] = probability
        item['accuracy'] = accuracy
        item.update(kwargs)

        dir[ref] = item
        self._bb[dir_key] = dir
        return item
    
    @authorized_method
    def set_items(self, items: List[BBItemDict], auth_token: str = None) -> List[BBItemDict]:
        return [self.set_item(**item, auth_token=auth_token) for item in items]
    
    @authorized_method
    def get_item(self, ref: str, auth_token: str = None) -> EBBItemDict:
        dir_key = auth_token or 'default'
        dir = self._bb.get(dir_key, {})
        item = dir.get(ref)
        if item is None:
            return self.empty_item
        return item
    
    @authorized_method
    def get_items(self, refs: List[str], auth_token: str = None) -> List[EBBItemDict]:
        return [self.get_item(ref, auth_token=auth_token) for ref in refs]
    
    @authorized_method
    def get_all_items(self, auth_token: str = None) -> List[BBItemDict]:
        dir_key = auth_token or 'default'
        dir = self._bb.get(dir_key, {})
        return list(dir.values())

    @property
    def empty_item(self):
        item: EBBItemDict = {}
        item['ref'] = None
        item['value'] = None
        item['belief'] = None
        item['probability'] = None
        item['accuracy'] = None
        return item