from stagecraft.apps.datasets.models import DataGroup, DataSet, DataType
import reversion


class CopyDatasetWithNewMapping(object):
    def map_one_to_one_fields(mapping, pairs):
        """
        >>> mapping = {'a': 'b'}
        >>> pairs = {'a': 1}
        >>> map_one_to_one_fields(mapping, pairs)
        {'b': 1}
        >>> mapping = {'a': ['b', 'a']}
        >>> map_one_to_one_fields(mapping, pairs)
        {'a': 1, 'b': 1}
        """
        mapped_pairs = dict()
        for key, value in pairs.items():
            if key in mapping:
                targets = mapping[key]
                if not isinstance(targets, list):
                    targets = list(targets)
                for target in targets:
                    mapped_pairs[target] = value
            else:
                mapped_pairs[key] = value

        return mapped_pairs

    def apply_mapping(mapping, pairs):
        logging.warn("{} -- {}".format(mapping, pairs))
        return dict(map_one_to_one_fields(mapping, pairs).items())
