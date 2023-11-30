const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const path = require('path');

const app = express();
const port = 3001;

app.use(cors());
app.use(express.static(path.join(__dirname, '../public')));
app.use(express.json());

app.post('/runPython', (req, res) => {
  const inputCharacter = req.body.character;
  const pythonScriptPath = path.join(__dirname, '../python/image_gen.py');

  process.chdir(path.join(__dirname, '../python/'));

  const pyProg = spawn('python3.11', [pythonScriptPath, inputCharacter]);

  let scriptOutput = '';
  pyProg.stdout.on('data', (data) => {
    scriptOutput += data.toString();
  });

  pyProg.on('close', (code) => {
    const outputLines = scriptOutput.trim().split('\n');
    const composedImagePath = outputLines[0];
    const strokeImagePath = outputLines[1];
    const svgPaths = JSON.parse(outputLines[2] || '[]');

    if (composedImagePath === 'Image generation failed' || !strokeImagePath) {
      console.error('Image generation failed');
      res.status(500).send('Image generation failed');
    } else {
      res.send({ 
        composedImagePath: `/images/generated_image.png`,
        strokeImagePath: `/images/stroke_image.png`,
        svgPaths 
      });
    }
  });

  pyProg.stderr.on('data', (data) => {
    console.error(`Error in Python script: ${data}`);
    res.status(500).send('Error in Python script');
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
