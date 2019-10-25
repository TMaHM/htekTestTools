# 自动化测试接口文档

> 为什么有这个文档？
> 因为《自动化测试 Action URI 说明V3.2》这个文档不够全


## 格式约定

> 这里列出所有接口，格式约定如下：
>
> 首先给出一个通用型的url，变量以 `$xxx` 的形式表示
>
> 接着给出一个具体的示例
>
> 最后列出所有接受的参数
>
> 如果有备注，以 Note：开头


## 1. 设置P值

`http://$usr:$pwd@$IP/AutoTest&setting=$P_code=$P_value`

`http://admin:admin@10.3.3.18/AutoTest&setting=P213=1`


==接受的值==：

$P_code：所有Pcode

$P_value：该P cdoe接受的值

> NOTE：
>
> P_value当然可以随意填值，只是会造成不明的后果，比如限制输入为0-127的地方传入-1，web上显示变成了65535
>
> 因为目前自动化测试的目的不是为了测试异常值，所以暂时没考虑异常输入

---


## 2. 按键操作 

`http://$usr:$pwd@$IP/AutoTest&keyboard=$key`

`http://admin:admin@10.3.3.18/AutoTest&keyboard=SPEAKER`


==接受的值==：

LineKey: 第一个为L1，以此类推

SoftKey：第一个为F1，以此类推

数字键：0-9

×号键：*

井号键：POUND

功能键区：F_HOLD，F_CONFERENCE，MUTE，MSG，HEADSET，SPEAKER，RD，DNDOn，DNDOff

导航键区：OK，X，UP，DOWN，LEFT，RIGHT

音量键：VOLUME_UP，VOLUME_DOWN

Reboot：Reboot

---


## 3. 拨号

`http://$usr:$pwd@$IP/AutoTest&keyboard=BASICCALL:NUMBER=$number`

`http://admin:admin@10.3.3.18/AutoTest&keyboard=BASICCALL:NUMBER=2055`

这个接口会以当前选择的账号拨出，不方便使用

当前推荐以老的URL拨号

`http://$usr:$pwd/$IP/Phone_ActionURL&Command=1&Number=$number&Account=$line`

`http://admin:admin@10.3.3.18/Phone_ActionURL&Command=1&Number=2055&Account=3`


==接受的值==：

$number：目标号码

$line：要以第几个Account拨出

---


## 4. 扩展板

`http://$usr:$pwd@$IP/AutoTest&keyboard=EXPANSION:EXP_NO:$expEXP_PAGE:$pageEXP_KEYNO:$key`

`http://admin:admin@10.3.3.18/AutoTest&keyboard=EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:0`


==接受的值==：

$exp：第几个扩展板

$page：第几页

$key：第几个key，从0开始

---


## 5. 检查img/rom信息

`http://$usr:$pwd@$IP/AutoTest&bsp=CHECKIMGINFO:$imginfo`

`http://admin:admin@10.3.3.18/AutoTest&bsp=CHECKIMGINFO:IMG--2.0.4.4.81(2019-09-21)15:30:00`



`http://$usr:$pwd@$IP/AutoTest&bsp=CHECKROMINFO:$rominfo`

`http://admin:admin@10.3.3.18/AutoTest&bsp=CHECKROMINFO:ROM--2.0.4.4.81(2019-09-21)15:30:00`


==接受的值==：

img和rom信息，注意时间格式，和web是不一样的

---


## 6. 检查GUI状态

`http://$usr:$pwd@$IP/AutoTest&gui=$CurMainWin=$Iconindex`

`http://user:1234@10.3.3.18/AutoTest&gui=LCD_Idle_Win:0`


==接受的值==

$CurMainWin：当前所处的界面

$IconIndex：当前选中的位置，开始为0，从上至下，从左至右，以此类推

> NOTE：
>
> Idle态时，$IconIndex可以是任意值

| LCD_Menu_Win          | LCD_Status_Win         | LCD_Information_Win     | LCD_Network_Win         |
| --------------------- | ---------------------- | ----------------------- | ----------------------- |
| LCD_Account_Win       | LCD_Feature_Win        | LCD_CallForword_Win     | LCD_AlwaysForword_Win   |
| LCD_BusyForword_Win   | LCD_NoAnswer_Win       | LCD_FunctionKey_Win     | LCD_LineasFunction_Win  |
| LCD_KeyasSend_Win     | LCD_HotLine_Win        | LCD_AnonymousCall_Win   | LCD_AnonymousSec_Win    |
| LCD_DND_Win           | LCD_RecordHistory_Win  | LCD_Directory_Win       | LCD_AllContacts_Win     |
| LCD_LocalContacts_Win | LCD_LDAPList_Win       | LCD_XMLList_Win         | LCD_BlackList_Win       |
| LCD_APList_Win        | LCD_MenuHistory_Win    | LCD_LocalHistory_Win    | LCD_AllCalls_Win        |
| LCD_MissedCalls_Win   | LCD_ReceiveCalls_Win   | LCD_DialCalls_Win       | LCD_ForWordCalls_Win    |
| LCD_CallLog_Win       | LCD_Message_Win        | LCD_VoiceMail_Win       | LCD_ViewVoiceMail_Win   |
| LCD_SetVoiceMail_Win  | LCD_SMS_Win            | LCD_ViewSMS_Win         | LCD_SetSMS_Win          |
| LCD_Settings_Win      | LCD_BasicSetting_Win   | LCD_Language_Win        | LCD_TimeDate_Win        |
| LCD_TimeFormat_Win    | LCD_DhcpTime_Win       | LCD_RingTone_Win        | LCD_HeadSet_Win         |
| LCD_Bluetooth_Win     | LCD_WiFi_Win           | LCD_AdvancedSetting_Win | LCD_AdvancedSetPass_Win |
| LCD_AccountPass_Win   | LCD_AdvanedNetwork_Win | LCD_WANPort_Win         | LCD_PCPort_Win          |
| LCD_Vlan_Win          | LCD_WebserverType_Win  | LCD_8021x_Win           | LCD_VPN_Win             |
| LCD_DhcpVlan_Win      | LCD_LLDP_Win           | LCD_PhoneSetting_Win    | LCD_Lock_Win            |
| LCD_SetPassword_Win   | LCD_AutoProvision_Win  | LCD_Display_Win         | LCD_DisplayMode_Win     |
| LCD_Wallpaper_Win     | LCD_Screensaver_Win    | LCD_OthersPass_Win      | LCD_OthersAPP_Win       |
| LCD_Factory_Win       | LCD_Restart_Win        | LCD_Reboot_Win          | LCD_PcapFeature_Win     |

---


## 7. DRD功能

`http://$usr:$pwd@$IP/AutoTest&drd=$operation`
`http://admin:admin@10.3.3.18/AutoTest&drd=RETURNIDLE`


### 1. 回到Idle态

==接受的值==：

**RETURNIDLE** 

`http://admin:admin@10.3.3.18/AutoTest&drd=RETURNIDLE`


### 2. Flexible Seating

==接受的值==：

**GUESTIN:aid=$aid&number=$number&password=$pwd**

`http://admin:admin@192.168.1.87/AutoTest&drd=GUESTIN:aid=0&number=0028&password=8606`

**GUESTOUT**

`http://admin:admin@192.168.1.87/AutoTest&drd=GUESTIN:aid=0&number=0028&password=8606	GUESTIN:aid=0&number=xxx&password=xxx`


> NOTE:
>
> aid一般为0，表示第一个Account


### 3. ACD

==接受的值==：

**ACD:LOGIN:aid=0**

`http://admin:admin@192.168.1.87/AutoTest&drd=ACD:LOGIN:aid=0`

**ACD:LOGOUT:aid=0** 

`http://admin:admin@192.168.1.87/AutoTest&drd=ACD:LOGOUT:aid=0`

**ACD:AVAILABLE:aid=0**

`http://admin:admin@192.168.1.87/AutoTest&drd=ACD:AVAILABLE:aid=0`

**ACD:UNAVAILABLE** 

`http://user:1234@192.168.1.87/AutoTest&drd=ACD:UNAVAILABLE`

**ACD:WRAPUP:aid=0**

`http://user:1234@192.168.1.87/AutoTest&drd=ACD:WRAPUP:aid=0	`

**ACD:DISPCODE**

`http://user:1234@192.168.1.87/AutoTest&drd=ACD:DISPCODE`

**ACD:CHECK:$status**

> ==接受的值==：
>
> IFLOGOUT
>
> IFUN_AVAILABLE
>
> IFAVAILABLE
>
> IFWRAPUP

`http://user:1234@192.168.1.87/AutoTest&drd=ACD:CHECK:IFLOGOUT`


### 4. Pickup

==接受的值==：

**CALLPICKUP:DPICK**

`http://user:1234@192.168.1.87/AutoTest&drd=CALLPICKUP:DPICK`

**CALLPICKUP:GPICK**

`http://user:1234@192.168.1.87/AutoTest&drd=CALLPICKUP:GPICK`


### 5. Call Park

==接受的值==：

**CALLPARK:DPARK**

`http://user:1234@192.168.1.87/AutoTest&drd=CALLPARK:DPARK`

**CALLPARK:GPARK**

`http://user:1234@192.168.1.87/AutoTest&drd=CALLPARK:GPARK`
