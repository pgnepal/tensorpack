# -*- coding: UTF-8 -*-
# File: config.py
# Author: Yuxin Wu <ppwwyyxx@gmail.com>

import tensorflow as tf
import six

from ..graph_builder import ModelDesc
from ..tfutils import get_default_sess_config
from ..tfutils.sessinit import SessionInit, JustCurrentSession
from ..tfutils.sesscreate import NewSessionCreator

__all__ = ['PredictConfig']


class PredictConfig(object):
    def __init__(self, model,
                 session_creator=None,
                 session_init=None,
                 input_names=None,
                 output_names=None,
                 return_input=False,
                 create_graph=True,
                 ):
        """
        Args:
            model (ModelDesc): the model to use.
            session_creator (tf.train.SessionCreator): how to create the
                session. Defaults to :class:`sesscreate.NewSessionCreator()`.
            session_init (SessionInit): how to initialize variables of the session.
                Defaults to do nothing.
            input_names (list): a list of input tensor names. Defaults to all
                inputs of the model.
            output_names (list): a list of names of the output tensors to predict, the
                tensors can be any computable tensor in the graph.
            return_input (bool): same as in :attr:`PredictorBase.return_input`.
            create_graph (bool): create a new graph, or use the default graph
                when then predictor is first initialized.
        """
        def assert_type(v, tp):
            assert isinstance(v, tp), v.__class__
        self.model = model
        assert_type(self.model, ModelDesc)

        if session_init is None:
            session_init = JustCurrentSession()
        self.session_init = session_init
        assert_type(self.session_init, SessionInit)

        if session_creator is None:
            self.session_creator = NewSessionCreator(config=get_default_sess_config())
        else:
            self.session_creator = session_creator

        # inputs & outputs
        self.input_names = input_names
        if self.input_names is None:
            raw_tensors = self.model.get_inputs_desc()
            self.input_names = [k.name for k in raw_tensors]
        self.output_names = output_names
        assert_type(self.output_names, list)
        assert_type(self.input_names, list)
        assert len(self.input_names), self.input_names
        for v in self.input_names:
            assert_type(v, six.string_types)
        assert len(self.output_names), self.output_names

        self.return_input = bool(return_input)
        self.create_graph = bool(create_graph)

    def _maybe_create_graph(self):
        if self.create_graph:
            return tf.Graph()
        return tf.get_default_graph()
