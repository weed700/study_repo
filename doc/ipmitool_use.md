# ipmitool useage

* 유저 확인
  * ipmitool user list 1
* 비밀 번호 변경
  * ipmitool user set password \<user id\> \<password\>
* 확인 방법 다른 노드에서
  * ipmitool -I lanplus -H \<IPMI IP\> -U \<user\> -P \<password\> chassis status
  * password에 !표가 들어가면 ''로 묶어서 입력 ex) ipmitool -P 'test!!'

### 참고 사이트
* https://www.intel.com/content/www/us/en/support/articles/000055688/server-products.html
* https://docs.oracle.com/cd/E19464-01/820-6850-11/IPMItool.html
