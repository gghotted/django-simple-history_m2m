from django.db import models
from simple_history.models import HistoricalRecords as _HistoricalRecords


@property
def updated_fields(self):
    if not self.prev_record:
        return []

    res = []
    curr = self
    prev = self.prev_record
    fields = self.instance_type._meta.fields
    m2m_track_fields = {
        '%s_list' % f.name 
        for f in self.instance_type._meta.many_to_many
    }
    for f in fields:
        curr_val = getattr(curr, f.name)
        prev_val = getattr(prev, f.name)
        if f.name in m2m_track_fields:
            name = f.name[:-5]
        else:
            name = f.name
        if prev_val != curr_val:
            res.append(name)
    return res


class HistoricalRecords(_HistoricalRecords):
    '''
    model의 attribute 순서에 영향을 받습니다.
    model의 가장 하단에 이 class를 생성하세요.
    반드시 "history"라는 이름으로 object를 저장하세요.
    '''
    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        
        for f in cls._meta.many_to_many:
            name = '%s_list' % f.name
            models.JSONField(null=True).contribute_to_class(cls, name)
            
    def create_history_model(self, model, inherited):
        model = super().create_history_model(model, inherited)
        setattr(model, 'updated_fields', updated_fields)
        return model
