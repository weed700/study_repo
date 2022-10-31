# yum repository 서버 만들기

* 필요 패키지 설치

```console
# yum install createrepo yum-utils
# yum install epel-release
# yum install nginx

# systemctl start nginx
# systemctl enable nginx
```
* 방화벽 & selinux 끄기

```console
# systemctl stop firewalld
# systemctl disable firewalld
# sed -i '/^SELINUX=/s/.*/SELINUX=disabled/' /etc/selinux/config
```

* 웹 브라우저를 통해 저장소와 패키지를 볼 수 있게 하기 위해서 `repos.conf` 구성 파일을 추가

```console
# vim /etc/nginx/conf.d/repos.conf
```

  * repos.conf 내용

```console
server {
        listen   80;
        server_name  repos.test.lab;	#change  test.lab to your real domain 
        root   /var/www/html/;
        location / {
                index  index.php index.html index.htm;
                autoindex on;	#enable listing of directory index
        }
}
```

* nginx 서버 restart
```console
# systemctl restart nginx
```

* 저장소 위치에서 createrepo 명령어를 통해 레포지토리 생성

```console
# mkdir /var/www/html/repo
# createrepo /var/www/html/repo

//레포지토리 추가
# vim /etc/yum.repos.d/repo-server.repo

/* 내용
[repo-server]
name=Repository server        
baseurl=file:///var/www/html/repo 
enabled=1
gpgcheck=0

//name=원하는 레포지토리 이름
//baseurl=file://레포지토리 경로
*/

//local에서 repository 확인
# yum clean all
# yum repository
```

* repository 업데이트 하여 신규 생성된 레포지토리 적용

```console
//원하는 패키지 저장소에 저장하기
# cd /var/www/html/repo
# [원하는 패키지 현재 위치에 저장]

# createrepo --update /var/www/html/repo
```

#### 구축한 repository 사용

* client에서 설정

```console
# vim /etc/yum.repos.d/repo-server.repo

[repo-server]
name=Repository server   
baseurl=http://192.168.9.30   
enabled=1
gpgcheck=0

//name=원하는 이름으로 지정
//baseurl=http://레포지토리서버IP
```


### 참고

[1] https://sky-h-kim.tistory.com/3
[2] https://ko.linux-console.net/?p=217
