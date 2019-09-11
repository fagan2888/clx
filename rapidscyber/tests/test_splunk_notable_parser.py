import cudf
import pandas
from rapidscyber.parsers.splunk_notable_parser import SplunkNotableParser

TEST_DATA = '1566345812.924, search_name="Test Search Name", orig_time="1566345812.924", info_max_time="1566346500.000000000", info_min_time="1566345300.000000000", info_search_time="1566305689.361160000", message.description="Test Message Description", message.hostname="msg.test.hostname", message.ip="100.100.100.123", message.user_name="user@test.com", severity="info", urgency="medium"'
TEST_DATA2 = '1548772230, search_name="Test Search Name 2", signature="Android.Adware.Batmobil", signature="Android.Adware.Dlv", signature="Android.PUP.Downloader", src="10.01.01.123", src="10.01.01.1", src_ip="10.01.01.123", src_ip="10.01.01.1, count="19", info_max_time="1548772200.000000000", info_min_time="1548599400.000000000", info_search_time="1548772206.179561000", info_sid="test-info-sid", lastTime="1548771235", orig_raw="<164>fenotify-113908.warning: CEF:0|FireEye|MPS|1.2.3.123|RC|riskware-callback|1|rt=Jan 29 2019 14:13:55 UTC end=Jan 29 2019 14:13:55 UTC src=10.01.01.123 dest="10.01.01.122" request=http://test.com/test.php cs1Label=sname cs1=Android.PUP.Downloader act=notified dvc=10.01.01.2 dvchost=fireeye.ban2-in smac=1a:2b:3c:4d:5e:6f dmac=1a:2b:3c:4d:5e:7g spt=49458 dpt=80 cn1Label=vlan cn1=0 externalId=123456 devicePayloadId=123abc msg=risk ware detected:57007 proto=tcp cs4Label=link cs4=https://fireeye.test/notification_url/test cs6Label=channel cs6=POST /multiadctrol.php HTTP/1.1::~~Content-type: application/json::~~User-Agent: Dalvik/2.1.0 (Linux; U; Android 8.0.0; SM-G611F Build/R16NW)::~~Host: test.hostname::~~Connection: Keep-Alive::~~Accept-Encoding: gzip::~~Content-Length: 85::~~::~~[{"android_id":"123abc","isnew":0,"m_ch":"123","s_ch":"1","ver_c":"342\\"}] \n\\\\x00", orig_sourcetype="source", src_subnet="12.34.56"'
TEST_DATA3 = '1548234811, search_name="Test Search Name 3", signature="Android.Adware.Batmobil", signature="Android.Adware.Dlv", signature="Android.PUP.Downloader", src="10.01.01.123", src="10.01.01.1", count="19", info_max_time="1548234811.000000000", info_min_time="1548599400.000000000", info_search_time="1548772206.179561000", info_sid="test-info-sid", lastTime="1548771235", orig_raw="<164>fenotify-113908.warning: CEF:0|FireEye|MPS|1.2.3.123|RC|riskware-callback|1|rt=Jan 29 2019 14:13:55 UTC end=Jan 29 2019 14:13:55 UTC src=10.01.01.123 dest="10.01.01.122" request=http://test.com/test.php cs1Label=sname cs1=Android.PUP.Downloader act=notified dvc=10.01.01.2 dvchost=fireeye.ban2-in smac=1a:2b:3c:4d:5e:6f dmac=1a:2b:3c:4d:5e:7g spt=49458 dpt=80 cn1Label=vlan cn1=0 externalId=123456 devicePayloadId=123abc msg=risk ware detected:57007 proto=tcp cs4Label=link cs4=https://fireeye.test/notification_url/test cs6Label=channel cs6=POST /multiadctrol.php HTTP/1.1::~~Content-type: application/json::~~User-Agent: Dalvik/2.1.0 (Linux; U; Android 8.0.0; SM-G611F Build/R16NW)::~~Host: test.hostname::~~Connection: Keep-Alive::~~Accept-Encoding: gzip::~~Content-Length: 85::~~::~~[{"android_id":"123abc","isnew":0,"m_ch":"123","s_ch":"1","ver_c":"342\\"}] \n\\\\x00", orig_sourcetype="source", src_subnet="12.34.56"'


def test_splunk_notable_parser():
    """Test splunk notable parsing"""

    snp = SplunkNotableParser()
    test_input_df = cudf.DataFrame()
    raw_colname = "_raw"

    test_input_df[raw_colname] = [TEST_DATA]
    test_output_df = snp.parse(test_input_df, raw_colname)
    assert len(test_output_df.columns) == 24
    assert test_output_df["time"][0] == "1566345812.924"
    assert test_output_df["search_name"][0] == "Test Search Name"
    assert test_output_df["orig_time"][0] == "1566345812.924"
    assert test_output_df["urgency"][0] == "medium"
    assert test_output_df["user"][0] == ""
    assert test_output_df["owner"][0] == ""
    assert test_output_df["security_domain"][0] == ""
    assert test_output_df["severity"][0] == "info"
    assert test_output_df["src_ip"][0] == ""
    assert test_output_df["src_mac"][0] == ""
    assert test_output_df["src_port"][0] == ""
    assert test_output_df["dest_ip"][0] == ""
    assert test_output_df["dest_port"][0] == ""
    assert test_output_df["dest_mac"][0] == ""
    assert test_output_df["dest_priority"][0] == ""
    assert test_output_df["device_name"][0] == ""
    assert test_output_df["event_name"][0] == ""
    assert test_output_df["event_type"][0] == ""
    assert test_output_df["id"][0] == ""
    assert test_output_df["ip_address"][0] == ""
    assert test_output_df["message_ip"][0] == "100.100.100.123"
    assert test_output_df["message_username"][0] == "user@test.com"
    assert test_output_df["message_hostname"][0] == "msg.test.hostname"
    assert test_output_df["message_description"][0] == "Test Message Description"

    test_input_df2 = cudf.DataFrame()
    test_input_df2[raw_colname] = [TEST_DATA2]
    test_output_df2 = snp.parse(test_input_df2, raw_colname)
    assert len(test_output_df2.columns) == 24
    assert test_output_df2["time"][0] == "1548772230"
    assert test_output_df2["search_name"][0] == "Test Search Name 2"
    assert test_output_df2["orig_time"][0] == ""
    assert test_output_df2["urgency"][0] == ""
    assert test_output_df2["user"][0] == ""
    assert test_output_df2["owner"][0] == ""
    assert test_output_df2["security_domain"][0] == ""
    assert test_output_df2["severity"][0] == ""
    assert test_output_df2["src_ip"][0] == "10.01.01.123"
    assert test_output_df2["src_mac"][0] == "1a:2b:3c:4d:5e:6f"
    assert test_output_df2["src_port"][0] == ""
    # dest_ip is obtained from dest attribute. Since data doesn't have dest_ip.
    assert test_output_df2["dest_ip"][0] == "10.01.01.122"
    assert test_output_df2["dest_mac"][0] == "1a:2b:3c:4d:5e:7g"
    assert test_output_df2["dest_port"][0] == ""
    assert test_output_df2["dest_priority"][0] == ""
    assert test_output_df2["device_name"][0] == ""
    assert test_output_df2["event_name"][0] == ""
    assert test_output_df2["event_type"][0] == ""
    assert test_output_df2["id"][0] == ""
    assert test_output_df2["ip_address"][0] == ""
    assert test_output_df2["message_ip"][0] == ""
    assert test_output_df2["message_username"][0] == ""
    assert test_output_df2["message_hostname"][0] == ""
    assert test_output_df2["message_description"][0] == ""

    test_input_df3 = cudf.DataFrame()
    test_input_df3[raw_colname] = [TEST_DATA3]
    test_output_df3 = snp.parse(test_input_df3, raw_colname)
    assert len(test_output_df3.columns) == 24
    assert test_output_df3["time"][0] == "1548234811"
    assert test_output_df3["search_name"][0] == "Test Search Name 3"
    assert test_output_df3["orig_time"][0] == ""
    assert test_output_df3["urgency"][0] == ""
    assert test_output_df3["user"][0] == ""
    assert test_output_df3["owner"][0] == ""
    assert test_output_df3["security_domain"][0] == ""
    assert test_output_df3["severity"][0] == ""
    # src_ip is obtained from src attribute. Since data doesn't have src_ip.
    assert test_output_df3["src_ip"][0] == "10.01.01.123"
    assert test_output_df3["src_mac"][0] == "1a:2b:3c:4d:5e:6f"
    assert test_output_df3["src_port"][0] == ""
    # dest_ip is obtained from dest attribute. Since data doesn't have dest_ip.
    assert test_output_df3["dest_ip"][0] == "10.01.01.122"
    assert test_output_df3["dest_mac"][0] == "1a:2b:3c:4d:5e:7g"
    assert test_output_df3["dest_port"][0] == ""
    assert test_output_df3["dest_priority"][0] == ""
    assert test_output_df3["device_name"][0] == ""
    assert test_output_df3["event_name"][0] == ""
    assert test_output_df3["event_type"][0] == ""
    assert test_output_df3["id"][0] == ""
    assert test_output_df3["ip_address"][0] == ""
    assert test_output_df3["message_ip"][0] == ""
    assert test_output_df3["message_username"][0] == ""
    assert test_output_df3["message_hostname"][0] == ""
    assert test_output_df3["message_description"][0] == ""
