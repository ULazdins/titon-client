FilterChangeActivity
    SF1 ?
    SF01%03d ?

FunMainActivity
    L
    Z - ja saņem <zck>

    SD01 - SD07 - dabūt datumus?
    F1-F4 - uzstādīt ātrumus

    ST0xxxx - uzstādīt taimeri? - "Please confirm that you want to update the aura-t display time and day?"

OtherSettingActivity
    SK10 - virtuves taimeris
    SW10 - vannas taimeris

    SW0xxx, SK0xxx - uzstādīt taimerus uz xxx (0-100)

PHSettingActivity
    SH1000 - nolasa mitruma līmeni
        atbild ar SH065040 - 65%

    SH0xxx - uzstāda mitruma līmeni

PwmSettingActivity
    Gaisa intake/outtake
    C010 - C710

    CS - uzsāk transaction?
    C00xxxx - uzstāda gaisa intake, outtake xxxx (0-100)
    CE - beidz transaction? Vai arī nobloķē edit, atbloķē edit?

SummerSettingActivity

    SS1000 - initial message?, atgriež SS 190 056, kur no 190 - 19.0 grādi

    SE1000 - atgriež SE 250 033, kur 250 - 25.0 grādi

    SB10 - atgriež SB 0 033, kur 0 ir "Summer boost disable" izslēgts


    SBx - ieslēgt/izslēgt summer bypass

    SE0xxx - uzstādīt Summer Extract
    SS0xxx - uzstādīt Summer Supply

SwitchSelectActivity
    X010 - X410 - četri slēdžu uzstādījumi - atbild ar X 2 05 111, kur 2 - slēdža kods (no pieprasījuma, 05 - istabas kods)


        1 - getString(R.string.wetRoomBoost), 
        2- getString(R.string.kitchenBoost), 
        getString(R.string.setBack), ??
        getString(R.string.summerBoostDisable), 
        getString(R.string.fanSpeed4), 
        getString(R.string.fansOff_o), "Fans off (N/O)"
        getString(R.string.fansOff_c), "Fans off (N/C)"
        8 - getString(R.string.manualSummerBypass)


    X00xx - saglabā slēdža uzstādījumus, xx - istabas kods

TimerSetActivity
    TM1 - nolasa taimera statusu, saņem TM1 0 40, kur 0 - nav ieslēgts
    TM0x - uzstāda taimer uz x







message_get_fan_1_speed_in = get_full_message("C010")
message_get_fan_1_speed_out = get_full_message("C110")
message_get_fan_2_speed_in = get_full_message("C210")
message_get_fan_2_speed_out = get_full_message("C310")
message_get_fan_3_speed_in = get_full_message("C410")
message_get_fan_3_speed_out = get_full_message("C510")
message_get_fan_4_speed_in = get_full_message("C610")
message_get_fan_4_speed_out = get_full_message("C710")


message_get_fan_speed = get_full_message("L")
message_get_fan_speed_ack = f":DAT|{hrv_mac}|{my_mac}|PS"
