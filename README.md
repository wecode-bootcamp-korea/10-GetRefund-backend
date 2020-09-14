## ✅ GetSuperFluid Clone Project

![Image of Superfluid](https://media.vlpt.us/images/ifyouseeksoomi/post/6d5bccf7-1bcb-4a0e-8e04-ef6be2ce69e2/%E1%84%87%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A9%E1%84%80%E1%85%B3%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5.png) <br>
이탈리안 코스메틱 브랜드 Superfluid 웹사이트(https://getsuperfluid.com/) 클론 프로젝트입니다. <br>

Frontend: 김신영, 박예진, 최운정 <br>
Backend: 안솔, 황수미 <br>
작업기간: 2주 (2020.08.03 - 2020.08.14) <br>

## Stack
- Language & Framwork: Python, Django Web framework
- Web Crawling: BeautifulSoup, Selenium
- Token: Bcrypt, JWT, KAKAO social login
- Database: MySQL
- CORS(Cross Origin Resource Sharing) headers
- AWS EC2, RDS
- Co-op: Github, Slack, Trello

## Demo
click the link to see our demo!
[![Watch the Demo](https://youtu.be/Ivby98Jlefk)](https://www.youtube.com/embed/Ivby98Jlefk)

## Database Modeling
<img src="https://media.vlpt.us/images/ifyouseeksoomi/post/43875543-3e77-48ce-9ca0-cdf76375b90a/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202020-09-14%20%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB%2011.40.38.png">

## Features
1. User
- [POST] SignUpView
- [POST] SignInView
- [POST] MyOrder - OrderCompleteView
- [GET] MyOrder - OrderedItemsView
- [GET] MyPage - FirstNameView
- [GET] KakaoLoginView

2. Product
- [GET] ProductListView
- [GET] ProductFilterView
- [GET] DetailInfoView
- [GET] PairWithView
- [GET] ProductDetailView

3. Order
- [POST] Cart - AddItemView
- [GET] Cart - CartListView
- [PATCH] Cart - CartItemEditView
- [DELETE] Cart - CartItemRemoveView
- [GET] RecommendItemView
- [GET] TotalItemQuantityView

