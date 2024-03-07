/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection, Contents } from '@jupyterlab/services';

/**
 * Document session endpoint provided by `jupyter_collaboration`
 * See https://github.com/jupyterlab/jupyter_collaboration
 */
const DOC_SESSION_URL = 'api/collaboration/session';
const DOC_FORK_URL = 'api/collaboration/fork_room';
const DOC_MERGE_URL = 'api/collaboration/merge_room';

/**
 * Document session model
 */
export interface ISessionModel {
  /**
   * Document format; 'text', 'base64',...
   */
  format: Contents.FileFormat;
  /**
   * Document type
   */
  type: Contents.ContentType;
  /**
   * File unique identifier
   */
  fileId: string;
  /**
   * Server session identifier
   */
  sessionId: string;
}

export async function requestDocSession(
  format: string,
  type: string,
  path: string
): Promise<ISessionModel> {
  const settings = ServerConnection.makeSettings();
  const url = URLExt.join(
    settings.baseUrl,
    DOC_SESSION_URL,
    encodeURIComponent(path)
  );
  const body = {
    method: 'PUT',
    body: JSON.stringify({ format, type })
  };

  let response: Response;
  try {
    response = await ServerConnection.makeRequest(url, body, settings);
  } catch (error) {
    throw new ServerConnection.NetworkError(error as Error);
  }

  let data: any = await response.text();

  if (data.length > 0) {
    try {
      data = JSON.parse(data);
    } catch (error) {
      console.log('Not a JSON response body.', response);
    }
  }

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response, data.message || data);
  }

  return data;
}


export async function requestDocFork(
  roomid: string,
): Promise<any> {
  const settings = ServerConnection.makeSettings();
  const url = URLExt.join(
    settings.baseUrl,
    DOC_FORK_URL,
    encodeURIComponent(roomid)
  );
  const body = {method: 'PUT'};

  let response: Response;
  try {
    response = await ServerConnection.makeRequest(url, body, settings);
  } catch (error) {
    throw new ServerConnection.NetworkError(error as Error);
  }

  let data: any = await response.text();

  if (data.length > 0) {
    try {
      data = JSON.parse(data);
    } catch (error) {
      console.log('Not a JSON response body.', response);
    }
  }

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response, data.message || data);
  }

  return data;
}


export async function requestDocMerge(
  forkRoomid: string,
  rootRoomid: string
): Promise<any> {
  const settings = ServerConnection.makeSettings();
  const url = URLExt.join(
    settings.baseUrl,
    DOC_MERGE_URL
  );
  const body = {
    method: 'PUT',
    body: JSON.stringify({ fork_roomid: forkRoomid, root_roomid: rootRoomid })
  };

  let response: Response;
  try {
    response = await ServerConnection.makeRequest(url, body, settings);
  } catch (error) {
    throw new ServerConnection.NetworkError(error as Error);
  }

  let data: any = await response.text();

  if (data.length > 0) {
    try {
      data = JSON.parse(data);
    } catch (error) {
      console.log('Not a JSON response body.', response);
    }
  }

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response, data.message || data);
  }

  return data;
}
