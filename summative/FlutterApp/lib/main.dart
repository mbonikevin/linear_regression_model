import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Score Predictor',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF3E7E4D)),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _form = GlobalKey<FormState>();
  final url = 'https://linear-regression-model-ihll.onrender.com/predict';

  final hours = TextEditingController();
  final attendance = TextEditingController();
  final prevScores = TextEditingController();
  final tutoring = TextEditingController();
  final physical = TextEditingController();

  String? involvement, resources, extra, internet, income, teacher, peer, disabilities, education, distance;

  bool busy = false;
  String result = '';
  bool isError = false;

  Future<void> sendPrediction() async {
    if (!_form.currentState!.validate()) return;
    setState(() { busy = true; result = ''; });

    final payload = {
      'hours_studied': int.parse(hours.text),
      'attendance': double.parse(attendance.text),
      'parental_involvement': involvement,
      'access_to_resources': resources,
      'extracurricular_activities': extra,
      'previous_scores': int.parse(prevScores.text),
      'internet_access': internet,
      'tutoring_sessions': int.parse(tutoring.text),
      'family_income': income,
      'teacher_quality': teacher,
      'peer_influence': peer,
      'physical_activity': int.parse(physical.text),
      'learning_disabilities': disabilities,
      'parental_education_level': education,
      'distance_from_home': distance,
    };

    try {
      final res = await http.post(Uri.parse(url),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode(payload));

      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        setState(() { result = 'Predicted Score: ${data['predicted_exam_score']}'; isError = false; });
      } else {
        setState(() { result = 'Something went wrong (${res.statusCode})'; isError = true; });
      }
    } catch (e) {
      setState(() { result = 'Could not reach server'; isError = true; });
    } finally {
      setState(() => busy = false);
    }
  }

  Widget field(String label, TextEditingController ctrl, {int min = 0, int max = 100}) {
    return TextFormField(
      controller: ctrl,
      keyboardType: TextInputType.number,
      decoration: InputDecoration(
        labelText: label,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
        isDense: true,
      ),
      validator: (v) {
        if (v == null || v.isEmpty) return 'required';
        final n = num.tryParse(v);
        if (n == null) return 'number only';
        if (n < min || n > max) return '$min–$max';
        return null;
      },
    );
  }

  Widget drop(String label, List<String> opts, String? val, void Function(String?) fn) {
    return DropdownButtonFormField<String>(
      initialValue: val,
      decoration: InputDecoration(
        labelText: label,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
        isDense: true,
      ),
      items: opts.map((o) => DropdownMenuItem(value: o, child: Text(o))).toList(),
      onChanged: fn,
      validator: (v) => v == null ? 'required' : null,
    );
  }

  Widget row(Widget a, Widget b) => Row(
    children: [Expanded(child: a), const SizedBox(width: 10), Expanded(child: b)],
  );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Student Score Predictor'),
        backgroundColor: const Color(0xFF3E7E4D),
        foregroundColor: Colors.white,
      ),
      body: Form(
        key: _form,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // result box
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: isError ? Colors.red.shade50 : result.isEmpty ? Colors.grey.shade100 : Colors.green.shade50,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: isError ? Colors.red.shade200 : result.isEmpty ? Colors.grey.shade300 : Colors.green.shade200),
              ),
              child: Text(
                result.isEmpty ? 'Fill the form and press Predict' : result,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: result.isEmpty ? 14 : 18,
                  fontWeight: result.isEmpty ? FontWeight.normal : FontWeight.bold,
                  color: isError ? Colors.red.shade700 : result.isEmpty ? Colors.grey : Colors.green.shade700,
                ),
              ),
            ),

            const SizedBox(height: 16),

            row(field('Hours Studied 1-44', hours, min: 1, max: 44), field('Attendance %', attendance, min: 0, max: 100)),
            const SizedBox(height: 10),
            field('Previous Scores %', prevScores, min: 0, max: 100), 
            const SizedBox(height: 10),
            field('Tutoring Sessions 0-8', tutoring, min: 0, max: 8),
            const SizedBox(height: 10),
            field('Physical Activity 0-6', physical, min: 0, max: 6),
            const SizedBox(height: 10),
            drop('Parental Involvement', ['Low', 'Medium', 'High'], involvement, (v) => setState(() => involvement = v)),
            const SizedBox(height: 10),
            drop('Access to Resources', ['Low', 'Medium', 'High'], resources, (v) => setState(() => resources = v)),
            const SizedBox(height: 10),
            row(drop('Family Income', ['Low', 'Medium', 'High'], income, (v) => setState(() => income = v)),
                drop('Teacher Quality', ['Low', 'Medium', 'High'], teacher, (v) => setState(() => teacher = v))),
            const SizedBox(height: 10),
            row(drop('Extracurricular', ['Yes', 'No'], extra, (v) => setState(() => extra = v)),
                drop('Internet Access', ['Yes', 'No'], internet, (v) => setState(() => internet = v))),
            const SizedBox(height: 10),
            row(drop('Learning Disabilities', ['Yes', 'No'], disabilities, (v) => setState(() => disabilities = v)),
                drop('Peer Influence', ['Negative', 'Neutral', 'Positive'], peer, (v) => setState(() => peer = v))),
            const SizedBox(height: 10),
            drop('Distance from Home', ['Near', 'Moderate', 'Far'], distance, (v) => setState(() => distance = v)),
            const SizedBox(height: 10),
            drop('Parental Education', ['High School', 'College', 'Postgraduate'], education, (v) => setState(() => education = v)),

            const SizedBox(height: 20),

            SizedBox(
              height: 50,
              child: ElevatedButton(
                onPressed: busy ? null : sendPrediction,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF3E7E4D),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: busy
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Text('Predict', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
