import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) { // 위젯을 사용하여
    return MaterialApp(
      // home: Icon(Icons.stars)
      // home: Text("텍스트")
      // home: Image.asset('emoticon.png')
      home: Center(
        child: Container( width: 50, height : 50, color: Colors.blue)
      )
    );
  }
}
