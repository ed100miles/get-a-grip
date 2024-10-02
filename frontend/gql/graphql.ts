/* eslint-disable */
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
  /** Date with time (isoformat) */
  DateTime: { input: any; output: any; }
};

export type Mutation = {
  __typename?: 'Mutation';
  addPinch: PinchType;
};


export type MutationAddPinchArgs = {
  deep: Scalars['Boolean']['input'];
  duration: Scalars['Float']['input'];
  weight: Scalars['Float']['input'];
  wide: Scalars['Boolean']['input'];
};

export type PinchType = {
  __typename?: 'PinchType';
  createdAt: Scalars['DateTime']['output'];
  deep: Scalars['Boolean']['output'];
  duration: Scalars['Float']['output'];
  id: Scalars['Int']['output'];
  userId: Scalars['Int']['output'];
  weight: Scalars['Float']['output'];
  wide: Scalars['Boolean']['output'];
};

export type Query = {
  __typename?: 'Query';
  pinches: Array<PinchType>;
};


export type QueryPinchesArgs = {
  createdAfter?: InputMaybe<Scalars['DateTime']['input']>;
  createdBefore?: InputMaybe<Scalars['DateTime']['input']>;
  deep?: InputMaybe<Scalars['Boolean']['input']>;
  maxDuration?: InputMaybe<Scalars['Float']['input']>;
  maxWeight?: InputMaybe<Scalars['Float']['input']>;
  minDuration?: InputMaybe<Scalars['Float']['input']>;
  minWeight?: InputMaybe<Scalars['Float']['input']>;
  userId?: InputMaybe<Scalars['Int']['input']>;
  wide?: InputMaybe<Scalars['Boolean']['input']>;
};

export type GetPinchesQueryVariables = Exact<{
  userId: Scalars['Int']['input'];
}>;


export type GetPinchesQuery = { __typename?: 'Query', pinches: Array<{ __typename?: 'PinchType', id: number, userId: number, wide: boolean, deep: boolean, weight: number, duration: number, createdAt: any }> };


export const GetPinchesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"GetPinches"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"userId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"pinches"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"userId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"userId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"userId"}},{"kind":"Field","name":{"kind":"Name","value":"wide"}},{"kind":"Field","name":{"kind":"Name","value":"deep"}},{"kind":"Field","name":{"kind":"Name","value":"weight"}},{"kind":"Field","name":{"kind":"Name","value":"duration"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}}]}}]}}]} as unknown as DocumentNode<GetPinchesQuery, GetPinchesQueryVariables>;