const { ipcMain } = require('electron');
const { SocketClient } = require('./sockets');
const { sequelize, Storage } = require('./models');

function createConnection(host, port) {
  const client = new SocketClient(host, port);
  ipcMain.on('send-data', (event, request) => {
    client.send(request);
    client.once(request.uid, (response) => {
      event.reply(response.uid, response);
    });
  });
  ipcMain
    .on('storage-get', (event, key) => {
      Storage.findOne({
        where: {
          key,
        },
      }).then((result) => {
        event.returnValue = result?.value ?? null;
      });
    })
    .on('storage-set', async (event, key, value) => {
      const [storage, created] = await Storage.findOrCreate({
        where: {
          key,
        },
        defaults: {
          value,
        },
      });
      if (!created) {
        await storage.update({
          value,
        });
        await storage.save();
      }
    })
    .on('storage-remove', async (event, key) => {
      const result = await Storage.findOne({
        where: {
          key,
        },
      });
      result?.destroy();
    });
  return client;
}

module.exports = {
  createConnection,
};
