# -*- coding: UTF-8 -*-
data1 = {"nodes":
    {
        "0" : {
            "ntype":"File",
                "sha1":"15ca429872d08b0986468c0dd37b366e56d5acba",
                "alias":["歐盟議程.pdf"],
                "subtype":["PDF"]
        },
        "1" : {
            "ntype":"File",
            "sha1":"38dba92472d08b0986468c0dd37b366e56d5acba",
            "alias":["a.exe"],
            "subtype":["EXE"]
        },
        "2" : {
            "ntype":"IP",
            "address":"33.44.55.66"
        },
        "3" : {
            "ntype":"IP",
            "address":"55.66.77.88"
        },
        "4" : {
            "ntype":"AutoRun",
            "key_value":"HKLM\\Software\\Microsoft\\Active Setup\\Installed Components\\<CLSID>"
        },
        "5" : {
            "ntype":"PseudoFile",
            "path":"C:\\Program File\\Internet Exploer\\iexplorer.exe"
        }
    },
    "edges":
    [
        {
            "subject_uid":"0",
                "object_uid":"1",
                "relation" : "drop"
        },
        {
            "subject_uid":"0",
            "object_uid":"1",
            "relation" : "createprocess",
            "tag" : ["cmd.exe /c c:/a.exe"]
        },
        {
            "subject_uid":"1",
            "object_uid":"2",
            "relation" : "connect"
        },
        {
            "subject_uid":"1",
            "object_uid":"3",
            "relation" : "connect"
        },
        {
            "subject_uid":"1",
            "object_uid":"4",
            "relation" : "reg"
        },
        {
            "subject_uid":"1",
            "object_uid":"5",
            "relation" : "inject"
        }
    ]
}

data2 = {"nodes":
    {
        "a" : {
            "ntype":"Email",
            "sha1":"389c129872d08b0986468c0dd37b366e56d5acba",
            "subject":"會議通知"
        },
        "b" : {
            "ntype":"InternetAccount",
            "address":"sender@example.com",
            "alias":["張三"]
        },
        "c" : {
            "ntype":"InternetAccount",
            "address":"receiver1@example.com",
            "alias":["李四"]
        },
        "d" : {
            "ntype":"InternetAccount",
            "alias":["王五"]
        },
        "e" : {
            "ntype":"File",
            "sha1":"aaaa429872d08b0986468c0dd37b366e56d5acba",
            "alias":["附件.zip"],
            "subtype":["ZIP"]
        },
        "f" : {
            "ntype":"File",
            "sha1":"15ca429872d08b0986468c0dd37b366e56d5acba",
            "alias":["議程.pdf"]
        }
    },
    "edges":
    [
        {
            "ntype":"link",
            "subject_uid":"b",
            "object_uid":"a",
            "relation":"send"
        },
        {
            "ntype":"link",
            "subject_uid":"c",
            "object_uid":"a",
            "relation":"receive",
            "tag":"to"
        },
        {
            "ntype":"link",
            "subject_uid":"d",
            "object_uid":"a",
            "relation":"receive",
            "tag":"cc"
        },
        {
            "ntype":"link",
            "subject_uid":"a",
            "object_uid":"e",
            "relation":"attachment"
        },
        {
            "ntype":"link",
            "subject_uid":"e",
            "object_uid":"f",
            "relation":"contain"
        }
    ]
}