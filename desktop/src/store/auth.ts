import { createStore } from 'effector';

interface ConnectionStore {
  token?: string;
  username?: string;
}

export const $auth = createStore<ConnectionStore>({});

const loadAccount = () => {};
