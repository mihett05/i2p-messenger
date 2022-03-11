import { v4 as uuid4 } from 'uuid';

const { getIpcRenderer, ipcOnce } = window.electronApi;

export interface BaseDataResponse {
  ok: boolean;
  error?: string;
}

export interface BaseResponse<T = BaseDataResponse> {
  action: string;
  uid: string;
  data: T;
}

export const request = <T = BaseDataResponse>(action: string, data: any): Promise<BaseResponse<T>> => {
  const uid = uuid4();
  getIpcRenderer().send('send-data', {
    action,
    uid,
    ...data,
  });
  return new Promise((resolve, reject) => {
    // TODO: reject and error handling
    ipcOnce(uid, (event: any, data: BaseResponse<T>) => {
      resolve(data);
    });
  });
};
