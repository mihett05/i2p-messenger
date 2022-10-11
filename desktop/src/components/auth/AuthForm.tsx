import React from 'react';
import { FormControl, FormLabel, Input } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';

interface IAuthForm {
  needPasswordAgain?: boolean;
}

function AuthForm({ needPasswordAgain }: IAuthForm) {
  const { register, handleSubmit, watch } = useForm();

  const onSubmit = handleSubmit((data) => {});

  return (
    <form onSubmit={onSubmit}>
      <FormControl>
        <FormLabel htmlFor="login">Login</FormLabel>
        <Input id="login" {...register('login')} />
      </FormControl>
      <FormControl>
        <FormLabel htmlFor="password">Password</FormLabel>
        <Input id="password" {...register('password')} />
      </FormControl>

      {needPasswordAgain && (
        <FormControl>
          <FormLabel htmlFor="password-again">Password(again)</FormLabel>
          <Input id="password-again" {...register('passwordAgain')} />
        </FormControl>
      )}
    </form>
  );
}

export default AuthForm;
