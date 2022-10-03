#encoding=utf-8

import grpc
from django.core.management.base import BaseCommand
from concurrent import futures
from service.savourrpc import chaineye_pb2_grpc
from service.grpc_server import ChaineyeServer


class Command(BaseCommand):
    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chaineye_pb2_grpc.add_ChaineyeServiceServicer_to_server(
            ChaineyeServer(),
            server
        )
        server.add_insecure_port('[::]:50252')
        server.start()
        print("start chaineye rpc")
        server.wait_for_termination()