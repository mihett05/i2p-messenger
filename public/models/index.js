const Storage = require('./storage');
const Message = require('./messages');
const User = require('./users');
const sequelize = require('./db');

module.exports = {
  Storage,
  Message,
  User,
  sequelize,
};
