from django.core.management.base import BaseCommand
from apps.absent.models import AbsentType

class Command(BaseCommand):
    def handle(self, *args, **options):
        absent_types = ["事假", "病假", "工伤假", "婚假", "丧假", "产假", "探亲假", "公假", "年休假"]
        for absent_type in absent_types:
            AbsentType.objects.create(name = absent_type)
        self.stdout.write("考勤类型数据初始化成功！")