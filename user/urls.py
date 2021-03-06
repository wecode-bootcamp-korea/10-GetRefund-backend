from django.urls import path
from .views import SignUpView, SignInView, MyOrder, MyPage, KakaoLoginView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/my-order', MyOrder.as_view()),
    path('/my-page', MyPage.as_view()),
    path('/kakao-signup', KakaoLoginView.as_view())
]

