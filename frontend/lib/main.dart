import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold( // 상중하 레이아웃으로 나누는 위젯
        appBar: AppBar(
          title: Text('앱임'),
        ),
        body: Container(
          child: Text('안녕')
        ),
        bottomNavigationBar:
          BottomAppBar(
            child: Container (
                height : 60,
                child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children : [
                      Icon(Icons.phone),
                      Icon(Icons.message),
                      Icon(Icons.contact_page)
                    ]
                )
            )
          )
      ),
    );
  }
}
