import 'dart:typed_data';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'camera_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text(
          "두피 진단",
          textAlign: TextAlign.center
        ),
        centerTitle: true
      ),
      body:
        Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              SafeArea(
                child: Center(
                    child: ElevatedButton(
                      onPressed: () async {
                        await availableCameras().then((value) => Navigator.push(context,
                            MaterialPageRoute(builder: (_) => CameraPage(cameras: value))));
                        setState(() {
                        });
                      },
                      child: const Text("두피 촬영하기"),
                    )),
              ),
              Text(
                "스마트폰 현미경을 사용해 두피를 촬영하고 두피 유형을 진단 받으세요😊",
                style: TextStyle(fontSize: 18),
              ),
            ],
        )
      ),
    );
  }
}