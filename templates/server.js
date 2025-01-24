const express = require('express');
const bodyParser = require('body-parser');
const webPush = require('web-push');

const app = express();
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.send('Server is running!');
});


const publicVapidKey = 'BFi1SFYxevd7_vj8S_bRJpnDoSsoi4sj7wUTayhZGfzB-6k8MoVj2LYIRRmWQv9GrMl8vgRMWXLGz29zcVhhq5s';
const privateVapidKey = 'bkhTPmSJy6UOkwG3G3dEQO1Fud-IqQ3536NHl08waZ8';

webPush.setVapidDetails(
    'mailto:your-email@example.com',
    publicVapidKey,
    privateVapidKey
);

const subscriptions = [];

app.post('/subscribe', (req, res) => {
    const subscription = req.body;
    subscriptions.push(subscription);
    res.status(201).json({});
});

app.post('/send-notifications', (req, res) => {
    const notificationPayload = JSON.stringify({
        title: 'Reminder',
        body: req.body.message || 'Your task is due!',
    });

    subscriptions.forEach(subscription => {
        webPush
            .sendNotification(subscription, notificationPayload)
            .catch(error => console.error('Error sending notification:', error));
    });

    res.status(200).json({ message: 'Notifications sent.' });
});


// Starting server
const PORT = 5000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));