import { v4 as uuid4 } from 'uuid';
import { once } from '@tauri-apps/api/event';
import { invoke } from '@tauri-apps/api';

export interface BaseDataResponse {
  ok: boolean;
  error?: string;
}

export interface BaseResponse<T = BaseDataResponse> {
  action: string;
  uid: string;
  data: T;
}

interface ServerMessage {
  message: string; // json
}

export const request = <T = BaseDataResponse>(action: string, data: any): Promise<BaseResponse<T>> => {
  const uid = uuid4();

  return invoke('send_request', {
    data: JSON.stringify({
      action,
      uid,
      data,
    }),
  }).then(
    () =>
      new Promise<BaseResponse<T>>((resolve, reject) => {
        once<ServerMessage>('server_message', (event) => {
          const response = JSON.parse(event.payload.message) as BaseResponse<T>;
          if (response.uid === uid) resolve(response);
        }).catch(reject);
      }),
  );
};
