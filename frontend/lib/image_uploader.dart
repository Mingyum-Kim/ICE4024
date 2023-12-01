import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:camera/camera.dart';

class ImageUploader {
  static Future<String> uploadFile(XFile file) async {

    var uri = Uri.parse('http://localhost:5000/predict');
    var filename = file.path.split('/').last;
    var request = http.MultipartRequest('POST', uri)
      ..files.add(await http.MultipartFile.fromBytes(
        'file',
        await file.readAsBytes(),
        filename: filename,
        contentType: MediaType('image', "jpg"),
      ));

    var response = await request.send();

    if (response.statusCode == 200) {
      // 파일 업로드 성공
      return await response.stream.bytesToString();
    } else {
      // 파일 업로드 실패
      throw http.ClientException(
          'Failed to upload file. Status: ${response.statusCode}');
    }
  }
}