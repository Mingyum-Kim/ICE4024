import 'dart:typed_data';

import 'package:flutter/material.dart';

/// 촬영한 사진의 미리 보기 화면을 제공
class ResultPage extends StatelessWidget {
  const ResultPage({Key? key, required this.response, required this.picture}) : super(key: key);

  final String response;
  final Uint8List picture;

  /// How to using BLOB URL ...
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

              /// 촬영 이미지
              Image.memory(picture, fit: BoxFit.cover, width: 250),
              SafeArea(
                child: Text(

                  /// 진단 결과
                    "진단 결과"
                ),
              ),
            ],
          )
      ),
    );
  }
}