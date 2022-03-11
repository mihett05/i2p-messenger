const { ipcMain } = require('electron');
const { SocketClient } = require('./sockets');

function createConnection(host, port) {
  const client = new SocketClient(host, port);
  ipcMain.on('send-data', (event, request) => {
    client.send(request);
    client.once(request.uid, (response) => {
      event.reply(response.uid, response);
    });
  });
  return client;
}

module.exports = {
  createConnection,
};
