import { request, BaseDataResponse } from './request';

interface CreateAccountResponse extends BaseDataResponse {
  token?: string;
}

export const createAccount = async (login: string, password: string): Promise<string | null> => {
  const response = await request<CreateAccountResponse>('create_account', {
    login,
    password,
  });

  return response.data.token ?? null;
};

export const signInAccount = async (login: string, password: string): Promise<string | null> => {
  const response = await request<CreateAccountResponse>('signin_account', {
    login,
    password,
  });

  return response.data.token ?? null;
};
