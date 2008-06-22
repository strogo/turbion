# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django import newforms as forms
from turbion.feedback.models import Feedback

#from pantheon.supernovaforms.fields import CaptchaField

class FeedbackForm( forms.ModelForm ):
    class Meta:
        model = Feedback
        exclude = ( "solved", "ip", )
#FeedbackForm.base_fields[ "captcha" ] = CaptchaField( label = u"Проверка" )
