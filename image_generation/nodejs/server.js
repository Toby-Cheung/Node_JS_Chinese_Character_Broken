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

  const pyProg = spawn('python3.9', [pythonScriptPath, inputCharacter]);

  pyProg.stdout.on('data', (data) => {
    // Capture the image path sent by the Python script
    const imagePath = data.toString().trim(); // Trim any extra spaces or newlines
    if (imagePath === 'Image generation failed') {
      console.error('Image generation failed');
      res.status(500).send('Image generation failed');
    } else {
      console.log('Image generated successfully');
      // Sending the image path to the client
      res.send({ imagePath: `/images/generated_image.png` });
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
