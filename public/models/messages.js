const { Model, DataTypes } = require('sequelize');
const sequelize = require('./db');

class Message extends Model {}

Message.init(
  {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: false,
      allowNull: false,
    },
    sender: {
      type: DataTypes.INTEGER,
    },
    receiver: {
      type: DataTypes.INTEGER,
    },
    message: {
      type: DataTypes.TEXT,
    },
  },
  {
    sequelize,
    modelName: 'Message',
    tableName: 'messages',
  },
);

module.exports = Message;
