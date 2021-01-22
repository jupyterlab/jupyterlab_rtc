import Automerge, { Text } from "automerge";

export type Doc = {
  docId: string;
  textArea: Text;
}

export const initDocument = () => {
  return Automerge.init<Doc>();
}

export const initDocumentText = (): Doc => {
  return Automerge.from({
    docId: '',
    textArea: new Automerge.Text()}
  )
}

export const applyChanges = (doc: Doc, changes: Array<Array<number>>): Doc => {

  changes.forEach((chunk) => {
    doc = Automerge.applyChanges(doc, [new Uint8Array(Object.values(chunk))]);
  });

  return doc;
}

export const getChanges = (oldDoc: Doc, newDoc: Doc) => {
  return Automerge.getChanges(oldDoc, newDoc);
}

export const merge = (oldDoc: Doc, newDoc: Doc) => {
  return Automerge.merge(oldDoc, newDoc);
}

export const getHistory = (doc: Doc) => {
  return Automerge.getHistory(doc).map(state => [state.change.message, state.snapshot.textArea]);
}
