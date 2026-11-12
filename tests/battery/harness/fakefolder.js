// Stands in for the folder picker: a directory handle over the Vault files served by serve.py
window.__fakeVault = async () => {
  const list = await (await fetch('/vault-list.json')).json();
  const mkDir = name => ({ kind: 'directory', name, kids: new Map(),
    async *entries() { for (const e of this.kids) yield e; },
    async requestPermission() { return 'granted'; }, async queryPermission() { return 'granted'; } });
  const root = mkDir('261021_VAULT_USSA_S');
  for (const [p, size] of list) {
    const parts = p.split('/'); let d = root;
    for (const seg of parts.slice(0, -1)) { if (!d.kids.has(seg)) d.kids.set(seg, mkDir(seg)); d = d.kids.get(seg); }
    const name = parts[parts.length - 1];
    d.kids.set(name, { kind: 'file', name, size, async getFile() { const b = await (await fetch('/vault/' + p.split('/').map(encodeURIComponent).join('/'))).arrayBuffer(); return new File([b], name); } });
  }
  window.showDirectoryPicker = async () => root;
  // the page remembers the picked folder in IndexedDB; a stand-in handle can't be stored, so skip that one write
  const put = IDBObjectStore.prototype.put;
  IDBObjectStore.prototype.put = function (v, k) { if (k === 'folder') return {}; return put.call(this, v, k); };
  return list.length;
};
