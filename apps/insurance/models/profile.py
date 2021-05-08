from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .common import BaseModel, ImageField
from .user import User,AssessorUser


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    national_code = models.BigIntegerField(_('National code'), unique=True, blank=True,null=True)
    birthday = models.DateField(_('Birthday'), blank=True, null=True)
    gender = models.CharField(_('Gender'), max_length=1, choices=(('F', 'Female'), ('M', 'Male')), blank=True,
                              null=True)
    address = models.CharField(_('Address'), max_length=100, blank=True, null=True)
    national_card = ImageField(verbose_name=_('National card'), upload_to='media/', blank=True)
    birth_certificate = ImageField(verbose_name=_('Birthday certificate'), upload_to='media/', blank=True)

    def __str__(self):
        return f"{self.user.get_full_name}'s profile"





class EvaluationCase(models.Model):
    """
    Each profile can contain several evaluation files, each case for an incident
    """
    insurer = models.ForeignKey(User, related_name='eval_cases', on_delete=models.CASCADE)
    explanations = models.CharField(_('Explanations'), max_length=500, blank=True, null=True,
                                    help_text='Write your explanations about this Case')
    pending = models.BooleanField(default=True)  # if the case is still pending or not
    date_created = models.DateTimeField(default=timezone.now)
    assessor = models.ForeignKey(AssessorUser, related_name='evaluations', on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return f"{self.insurer.get_full_name}-eval{self.pk}"


class Attachment(models.Model):
    name = models.CharField(_('File name'), max_length=150)
    file = models.FileField(_('File'), upload_to="attachments")
    evaluation = models.ForeignKey(EvaluationCase, related_name='attachments', on_delete=models.CASCADE)
