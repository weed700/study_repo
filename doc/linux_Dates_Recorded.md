### 리눅스 Dates Recorded

* ctime(change time) : 파일이나 inode 값이 바뀐 시점(속성값이 바뀐 시점), 퍼미션이나 소유주, 파일 크기 등 파일 속성값이 변경되었을 때 ctime은 갱신됨
* mtime(modify time) : 파일의 수정 시간, 속성이 아닌 파일의 내용이 바뀌었을 때 이 값이 바뀜
 
  * 주의 할 것 : 
    * 파일의 내용이 바뀌면 파일의 크기가 달라진다. 이때 파일의 크기가 속성이므로 ctime도 갱신됨, 만약 파일을 수정했는데 파일의 크기가 변경되지 않았을 수도 있다. 하지만 mtime이 파일의 속성이므로 ctime도 바뀐다.
    * mtime이 갱신되면 ctime도 갱신된다. 하지만 ctime이 변경된다고 mtime이 변경되지는 않는다.

  * atime(access time) : 파일을 오픈(grep, sort, cat 등.. 명령을 주거나 open() 함수로 열었을 때를 의미함) 하면 atime이 갱신된다.

  * 파일의 ctime, mtime, atime을 쉘에서 stat 명령어로 확인
 
    * ex) stat [file name]

