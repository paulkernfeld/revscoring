"""
These meta-datasources operate on :class:`revscoring.Datasource`'s that
return `list`'s of items and produce vectors out of the same.

.. autoclass:: revscoring.datasources.meta.vectors
"""
import os.path

from gensim.models.keyedvectors import KeyedVectors

from ..datasource import Datasource

ASSET_SEARCH_DIRS = ["word2vec/", "~/.word2vec/", "/var/share/word2vec/"]
VECTOR_DIMENSIONS = 300
keyed_vecs = {}


class word2vec(Datasource):
    """
    Generates vectors for a list of items generated by another
    datasource.

    :Parameters:
        items_datasource : :class:`revscoring.Datasource`
            A datasource that returns a list of words.
        keyed_vectors : :class:`gensim.models.keyedvectors.KeyedVectors`
            loaded key-vectors.  See :func:`~revscoring.datasources.meta.vectorizers.word2vec.load_kv`
        name : `str`
            A name for the `revscoring.FeatureVector`
    """  # noqa

    def __init__(self, items_datasource, keyed_vectors, name=None):
        name = self._format_name(name, [items_datasource, keyed_vectors])
        keyed_vecs[name] = keyed_vectors
        super().__init__(name, self.process, depends_on=[items_datasource])

    def process(self, words):
        return [keyed_vecs[self.name][word] if word in
                keyed_vecs[self.name] else [0] * VECTOR_DIMENSIONS
                for word in words]

    @staticmethod
    def load_kv(filename=None, path=None, limit=None):
        if path is not None:
            return KeyedVectors.load_word2vec_format(
                path, binary=True, limit=limit)
        elif filename is not None:
            for dir_path in ASSET_SEARCH_DIRS:
                try:
                    path = os.path.join(dir_path, filename)
                    return KeyedVectors.load_word2vec_format(
                        path, binary=True, limit=limit)
                except FileNotFoundError:
                    continue
            raise FileNotFoundError("Please make sure that 'filename' \
                                    specifies the word vector binary name \
                                    in default search paths or 'path' \
                                    speficies file path of the binary")
        else:
            raise TypeError(
                "load_kv() requires either 'filename' or 'path' to be set.")
