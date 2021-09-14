# ESJZone-novel-mirror
ESJZone 的小說備份
ESJZone 下架了大量小說，於是寫了程式儘量把他們備份下來，以原來分類「日輕」的小說為主。

如想觀看ESJZone的鏡像網站, 你可以前往 <https://esjzone.cf> 觀看
如果你有舊的網站, 可以直接 吧 `esjzone.cc` 替換成 `esjzone.cf` 繼續觀看

### 備份格式
讀取小說的小說章節頁面，依該頁面的「站內連結」來做備份，並把它寫成一個 txt 文字檔，檔案名為該小說的小說名。
1. 純文字檔，不會紀錄任何非文字的內容，如插圖
2. 小說章節頁面如果為空，就不會備份任何章節
 同理，不顯示於小說章節頁面的章節也不會備份
3. 需要密碼的頁面不會備份
4. 非站內的超連結，僅會顯示該超連結，並不會備份此超連結內所指向的章節內容

### 備份使用工具
修改自 [ZALin/ESJ-novel-backup](https://github.com/ZALin/ESJ-novel-backup)

### 最後更新時間
2021/08/21 08:30 (UTC+8)
