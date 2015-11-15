from proso.models.item_selection import ItemSelection, DEFAULT_TARGET_PROBABILITY
import random
import math
import proso.django.log
import numpy
import logging
from collections import defaultdict


LOGGER = logging.getLogger('django.request')


class ScoreItemSelection(ItemSelection):

    def __init__(
            self, predictive_model, weight_probability=10.0, weight_number_of_answers=5.0,
            weight_time_ago=5, weight_parent_time_ago=5.0, weight_parent_number_of_answers=2.5,
            target_probability=DEFAULT_TARGET_PROBABILITY, time_ago_max=120, recompute_parent_score=True,
            history_adjustment=True, estimate_parent_factors=True):
        ItemSelection.__init__(self, predictive_model, target_probability, history_adjustment)
        self._weight_probability = weight_probability
        self._weight_number_of_answers = weight_number_of_answers
        self._weight_time_ago = weight_time_ago
        self._weight_parent_time_ago = weight_parent_time_ago
        self._weight_parent_number_of_answers = weight_parent_number_of_answers
        self._estimate_parent_factors = estimate_parent_factors
        self._recompute_parent_score = recompute_parent_score
        self._time_ago_max = time_ago_max

    def select(self, environment, user, items, time, practice_context, n, **kwargs):
        parents = dict(zip(items, environment.get_items_with_values_more_items('parent', items=items)))
        if self._estimate_parent_factors:
            related_items = items
        else:
            parent_ids = set(sum([[p for p, v in ps] for ps in parents.values()], []))
            children = dict(zip(parent_ids, environment.get_items_with_values_more_items('child', items=parent_ids)))
            related_items = sum([[i for i, v in c] for c in children.values()], [])
            parents = defaultdict(lambda:[])
            for parent, childs in children.items():
                for child, v in childs:
                    parents[child].append((parent, v))

        answers_num = dict(zip(related_items, environment.number_of_answers_more_items(user=user, items=related_items)))
        last_answer_time = dict(zip(related_items, environment.last_answer_time_more_items(user=user, items=related_items)))
        probability = self.get_predictions(environment, user, items, time)
        last_answer_time_parents = self._last_answer_time_for_parents(environment, parents, last_answer_time)
        answers_num_parents = self._answers_num_for_parents(environment, parents, answers_num)
        prob_target = self.get_target_probability(environment, user, practice_context=practice_context)

        if proso.django.log.is_active():
            for item in items:
                if len(parents.get(item, [])) == 0:
                    LOGGER.warn("The item %s has no parent" % item)

        def _score(item):
            return (
                self._weight_probability * self._score_probability(prob_target, probability[item]) +
                self._weight_time_ago * self._score_last_answer_time(last_answer_time[item], time) +
                self._weight_number_of_answers * self._score_answers_num(answers_num[item]),
                random.random()
            )

        def _finish_score(((score, r), i)):
            total = 0.0
            parent_time_score = 0.0
            parent_answers_num_score = 0.0
            for p, v in parents[i]:
                parent_time_score += v * self._score_last_answer_time(last_answer_time_parents[p], time)
                parent_answers_num_score += v * self._score_answers_num(answers_num_parents[p])
                total += 1
            if total > 0:
                parent_time_score = parent_time_score / total
                parent_answers_num_score = parent_answers_num_score / total
            score += self._weight_parent_time_ago * parent_time_score
            score += self._weight_parent_number_of_answers * parent_answers_num_score
            return (score, r), i

        scored = zip(map(_score, items), items)
        if self._recompute_parent_score:
            candidates = []
            while len(candidates) < n and len(scored) > 0:
                finished = map(_finish_score, scored)
                score, chosen = max(finished)
                if proso.django.log:
                    LOGGER.debug(
                        'selecting %s (total_score %.2f, prob: %.4f, prob score %.2f, time: %s, time_score %.2f, answers: %s, answers score %.2f, parents %s)' %
                        (
                            chosen, score[0],
                            probability[chosen],
                            self._weight_probability * self._score_probability(prob_target, probability[chosen]),
                            last_answer_time[chosen],
                            self._weight_time_ago * self._score_last_answer_time(last_answer_time[chosen], time),
                            answers_num[chosen],
                            self._weight_number_of_answers * self._score_answers_num(answers_num[chosen]),
                            map(lambda x: x[0], parents[chosen]))
                        )
                candidates.append(chosen)
                for p, v in parents[chosen]:
                    last_answer_time_parents[p] = time
                scored = filter(lambda (score, i): i != chosen, scored)
        else:
            candidates = map(lambda ((score, r), i): i, sorted(scored, reverse=True)[:min(len(scored), n)])

        return candidates, [None for _ in candidates]

    def _score_answers_num(self, answers_num):
        return 0.5 / max(math.sqrt(answers_num), 0.5)

    def _score_probability(self, target_probability, probability):
        diff = target_probability - probability
        sign = 1 if diff > 0 else -1
        normed_diff = abs(diff) / max(0.001, abs(target_probability - 0.5 + sign * 0.5))
        return 1 - normed_diff ** 2

    def _score_last_answer_time(self, last_answer_time, time):
        if last_answer_time is None:
            return 0.0
        seconds_ago = (time - last_answer_time).total_seconds()
        if seconds_ago <= 0:
            return -1.0
        return -1 + numpy.log2(min(seconds_ago, self._time_ago_max)) / numpy.log2(self._time_ago_max)

    def _answers_num_for_parents(self, environment, parents, answers_num):
        children = defaultdict(list)
        for i, ps in parents.iteritems():
            for p, v in ps:
                children[p].append(i)

        return dict(map(
            lambda (p, chs): (p, sum(map(lambda ch: answers_num[ch], chs))),
            children.items()))

    def _last_answer_time_for_parents(self, environment, parents, last_answer_time):
        children = defaultdict(list)
        for i, ps in parents.iteritems():
            for p, v in ps:
                children[p].append(i)

        def _max_time_from_items(xs):
            times = filter(lambda x: x is not None, map(lambda x: last_answer_time[x], xs))
            if len(times) > 0:
                return max(times)
            else:
                return None
        return dict(map(lambda (p, chs): (p, _max_time_from_items(chs)), children.items()))

    def __str__(self):
        return 'SCORE BASED ITEM SELECTION: target probability {0:.2f}, weight probability {1:.2f}, weight time {2:.2f}, weight answers {3:.2f}'.format(
            self._target_probability, self._weight_probability, self._weight_time_ago, self._weight_number_of_answers)
