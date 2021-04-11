import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:io' show Platform;
import 'package:flutter/services.dart';
import 'package:device_info/device_info.dart';
import 'package:crypto/crypto.dart';
import 'dart:convert' show utf8;
import 'package:http/http.dart' as http;

void main() {
  runApp(MainApp());
}

class MainApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lighting control app',
      theme: ThemeData(
        primarySwatch: Colors.amber,
      ),
      home: MyHomePage(title: 'Lighting control app'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;
  String _platfromIdSha256 = 'None';
  Map<int, bool> _switchStatuses = {1: false};
  String _base_url = 'http://192.168.1.104/';
  String _endpoint_addr = 'setPinValue';

  @override
  void initState() {
    super.initState();
    initPlatformState();
  }

  Future<void> initPlatformState() async {
    String platformId;
    String platfromIdSha256;

    // Platform messages may fail, so we use a try/catch PlatformException.
    try {
      platformId = await _getId();
      platfromIdSha256 = sha256.convert(utf8.encode(platformId)).toString();
    } on PlatformException {
      platfromIdSha256 = 'Failed to get Device MAC Address.';
    }

    if (!mounted) return;

    setState(() {
      _platfromIdSha256 = platfromIdSha256;
    });
  }

  Future<String> _getId() async {
    var deviceInfo = DeviceInfoPlugin();
    if (Platform.isIOS) {
      var iosDeviceInfo = await deviceInfo.iosInfo;
      return iosDeviceInfo.identifierForVendor; // unique ID on iOS
    } else {
      var androidDeviceInfo = await deviceInfo.androidInfo;
      return androidDeviceInfo.androidId; // unique ID on Android
    }
  }

  Future<http.Response> _sendPostLedControl(base_url, endpoint_addr, data) {
    return http.post(Uri.https(base_url, endpoint_addr),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: data);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SwitchListTile(
              title: const Text('Lights', style: TextStyle(fontSize: 25)),
              activeColor: Colors.yellowAccent,
              activeTrackColor: Colors.yellow,
              value: _switchStatuses[1],
              contentPadding: EdgeInsets.all(25),
              onChanged: (bool value) {
                setState(() {
                  _switchStatuses[1] = value;
                  // _sendPostLedControl(_base_url, _endpoint_addr,
                  //     {'token': _platfromIdSha256, 'pin': 1, 'value': value});
                });
              },
              secondary: const Icon(Icons.lightbulb_outline, size: 35.0),
            ),
          ],
        ),
      ),
    );
  }
}
