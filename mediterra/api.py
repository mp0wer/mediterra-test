# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from rest_framework import routers
from .viewsets import TeacherViewSet, StudentViewSet, GradeViewSet, SpecializationViewSet

router = routers.DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'specializations', SpecializationViewSet)

urlpatterns = router.urls
