import json

queriesDict = {'queries': [{'query': "SELECT FROM_UNIXTIME(timestamp/1000,'%Y-%m-%d') as day_with_data, count(*) as records FROM locations WHERE device_id = '24255b80-be4d-49b2-a514-f2ecff6a413a' GROUP by day_with_data", 'results': (('2014-02-13', 1407L), ('2014-02-14', 3699L), ('2014-02-15', 3911L), ('2014-02-16', 3880L), ('2014-02-17', 3960L), ('2014-02-18', 3764L), ('2014-02-19', 3769L), ('2014-02-20', 310L))}, {'query': "SELECT double_latitude, double_longitude FROM locations WHERE device_id = '24255b80-be4d-49b2-a514-f2ecff6a413a'", 'results': [[40.4436088, -79.945417800000001], [40.443400699999998, -79.944647399999994, 'on_bicycle', 8115.7460000000001], [40.443121329999997, -79.943910869999996], [40.442185590000001, -79.943866180000001], [40.441224609999999, -79.943978310000006, 'on_foot', 16694.248, 'still', 23559.806, 'tilting', 17604.297999999999, 'unknown', 17824.996999999999], [40.440882000000002, -79.943343299999995], [40.442019700000003, -79.942957199999995], [40.442840799999999, -79.942688799999999], [40.443378600000003, -79.942120700000004, 'in_vehicle', 653.83100000000002, 'on_bicycle', 0.0], [40.443954099999999, -79.9428968], [40.445114269999998, -79.942750259999997], [40.445897100000003, -79.942544799999993], [40.44696047, -79.942245040000003], [40.447899470000003, -79.937428819999994], [40.450689959999998, -79.930154090000002], [40.455480960000003, -79.932986909999997], [40.458826250000001, -79.928498959999999], [40.460219440000003, -79.923380420000001], [40.455704140000002, -79.921898170000006, 'tilting', 82176.546000000002, 'on_foot', 50129.921999999999, 'in_vehicle', 0.0, 'still', 84910.875, 'tilting', 84336.879000000001, 'unknown', 82684.587, 'still', 86182.561000000002, 'tilting', 69565.580000000002, 'unknown', 84057.301000000007, 'still', 86337.322, 'tilting', 85224.839999999997, 'unknown', 77848.436000000002, 'still', 6548.5029999999997, 'tilting', 5187.2460000000001, 'unknown', 5775.2860000000001], [40.45533975, -79.925261280000001], [40.455759389999997, -79.922780209999999], [40.4552847, -79.921300599999995, 'on_foot', 0.0, 'still', 84208.225000000006, 'unknown', 84098.654999999999, 'still', 84966.482000000004, 'tilting', 80751.323999999993, 'unknown', 83647.561000000002, 'in_vehicle', 1343.296, 'on_foot', 18469.223000000002, 'on_foot', 20388.999], [40.456007499999998, -79.919657900000004], [40.455579700000001, -79.920648900000003], [40.455199399999998, -79.922294300000004], [40.454595599999998, -79.922916999999998], [40.454172100000001, -79.9241435], [40.455370100000003, -79.923689400000001], [40.454632400000001, -79.921958099999998], [40.453103499999997, -79.925144299999999], [40.451712399999998, -79.928503500000005], [40.4503165, -79.929439900000006], [40.449973, -79.931073499999997], [40.454914899999999, -79.920073200000004], [40.456282600000002, -79.923519799999994], [40.455293699999999, -79.919495100000006], [40.4547715, -79.924158800000001], [40.456097300000003, -79.921341100000006], [40.455526200000001, -79.916750899999997], [40.454815099999998, -79.915544400000002], [40.454777399999998, -79.925512999999995], [40.455535300000001, -79.924518800000001], [40.456232700000001, -79.9244123], [40.457862900000002, -79.923990799999999], [40.4569987, -79.922348200000002], [40.457787799999998, -79.9223961], [40.458925499999999, -79.920721700000001], [40.459026639999998, -79.919107370000006], [40.459634299999998, -79.9192745], [40.459035, -79.919981199999995], [40.4596187, -79.921528899999998], [40.454627500000001, -79.911892399999999], [40.4546013, -79.926780699999995], [40.455550199999998, -79.9177842], [40.4547217, -79.9207933], [40.454459100000001, -79.924829599999995], [40.455970299999997, -79.9362098], [40.456317900000002, -79.9251668], [40.454903600000002, -79.918387999999993], [40.454232300000001, -79.916624200000001], [40.456379400000003, -79.922116700000004], [40.453968000000003, -79.921988999999996], [40.454204500000003, -79.919496600000002], [40.461619599999999, -79.937692699999999], [40.450563199999998, -79.9086298], [40.452857399999999, -79.920690800000003], [40.449172400000002, -79.932266499999997], [40.447572200000003, -79.9420559], [40.444494800000001, -79.942566499999998], [40.443375799999998, -79.943198600000002], [40.441673700000003, -79.945378099999999, 'in_vehicle', 646.13099999999997], [40.442841620000003, -79.945162969999998], [40.439436600000001, -79.9432039], [40.440769000000003, -79.944482399999998], [40.441291999999997, -79.947414100000003], [40.441736740000003, -79.949835660000005], [40.442391710000003, -79.951515569999998], [40.442737379999997, -79.953564749999998, 'in_vehicle', 79479.960999999996, 'on_foot', 81485.495999999999, 'still', 86310.199999999997, 'tilting', 86330.020999999993, 'unknown', 85690.880000000005], [40.442920149999999, -79.9527985], [40.443522850000001, -79.952444420000006], [40.443963840000002, -79.950144219999999], [40.444185060000002, -79.948904600000006], [40.444409870000001, -79.946426509999995], [40.444566459999997, -79.944766060000006], [40.445108169999997, -79.948121139999998], [40.448885480000001, -79.951694970000005], [40.452689399999997, -79.949045900000002], [40.456238329999998, -79.939425779999993], [40.45357516, -79.9352734], [40.458265410000003, -79.929934579999994], [40.460744179999999, -79.922467440000005], [40.454108580000003, -79.917900200000005], [40.454066840000003, -79.920813570000007], [40.453298699999998, -79.919457399999999], [40.453558350000002, -79.921439250000006], [40.456740400000001, -79.9167846], [40.456917199999999, -79.917732099999995], [40.455220599999997, -79.926024100000006], [40.452042400000003, -79.924100699999997], [40.450792219999997, -79.927559849999994], [40.450396499999997, -79.928226499999994], [40.448123889999998, -79.934858730000002], [40.447580299999998, -79.940682800000005], [40.441460990000003, -79.943247999999997], [40.443970399999998, -79.9443938], [40.451000729999997, -79.953105440000002], [40.452556039999997, -79.949833650000002], [40.455178770000003, -79.9417294], [40.455337380000003, -79.938110929999993], [40.456059449999998, -79.934005720000002], [40.459924700000002, -79.925588160000004], [40.455880000000001, -79.918775199999999], [40.456165200000001, -79.920533300000002], [40.451552499999998, -79.926038800000001], [40.448601500000002, -79.933983999999995], [40.441597100000003, -79.944629800000001], [40.441050300000001, -79.945768700000002], [40.449786099999997, -79.929834999999997], [40.458699199999998, -79.929233699999997], [40.456980299999998, -79.921211600000007], []]}]}


resList = queriesDict["queries"]
recordDict = resList[0]
recordList =  recordDict["results"]

targetList = []
for r in recordList:
	targetDict = {}	
	targetDict["date"] = r[0]
	targetDict["count"] = r[1]
	targetList.append(targetDict)

print targetList	

recordDict = resList[1]
recordList =  recordDict["results"]


actList = []
for r in recordList:
	if len(r) > 2:
		tmpDict = {}
		tmpDict["location"] = r[:2]
		r = r[2:]
		tmpList = []
		while len(r) > 0:
			tmpSubDict = {}
			tmpSubDict["activity"] = r[0];
			tmpSubDict["span"] = r[1];
			tmpList.append(tmpSubDict);
			r = r[2:]
		tmpDict["results"] = tmpList	
		actList.append(tmpDict)
print actList