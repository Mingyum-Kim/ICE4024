import 'package:flutter/material.dart';
import 'package:camera/camera.dart';

Future<void> main() async {
  // 비동기 데이터를 다룸으로서 아래 코드를 추가한다.
  // 다음에 호출되는 함수가 모두 실행이 끝날 때까지 기디린다.
  WidgetsFlutterBinding.ensureInitialized();
  // 기기에서 사용 가능한 카메라 목록 불러오기
  final cameras = await availableCameras();
  // 사용 가능한 카메라 중 첫 번째 카메라 사용
  final firstCamera = cameras.first;
  runApp(
    MaterialApp(
      theme: ThemeData.dark(),
      home: MyApp (
        camera: firstCamera,
      ),
    ),
  );
}

class MyApp extends StatefulWidget {
  const MyApp({
    super.key,
    required this.camera,
  });

  final CameraDescription camera;

  @override
  MyAppState createState() => MyAppState();
}

class MyAppState extends State<MyApp> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    // 카메라 관리하는 컨트롤러 생성
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.medium,
    );
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: const Text('카메라 화면')),
        body: Column(
          children: [
            FutureBuilder<void>(
              future: _initializeControllerFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.done) {
                  // 미리보기
                  return CameraPreview(_controller);
                } else {
                  return const Center(child: CircularProgressIndicator());
                }
              },
            ),
          ],
        ),

        // 버튼 누를 시 카메라 화면의 캡쳐본을 보여주는 화면으로 이동
        floatingActionButton: FloatingActionButton(
          onPressed: () async {
            try {
              await _initializeControllerFuture;
              // 현재 카메라 화면 캡쳐
              final image = await _controller.takePicture();
              if (!mounted) return;
              // 사진 보여주기
              await Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (context) => DisplayPictureScreen(
                    imagePath: image.path,
                  ),
                ),
              );
            } catch (e) {
              print(e);
            }
          },
          child: const Icon(Icons.camera_alt),
        ),
      );
    }
}

class DisplayPictureScreen extends StatelessWidget {
  final String imagePath;

  const DisplayPictureScreen({super.key, required this.imagePath});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('캡쳐 화면')),
      body: Image.file(File(imagePath)),
    );
  }
}