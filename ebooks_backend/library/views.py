from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Book, ReadingProgress
from .serializers import (
    BookListSerializer, BookDetailSerializer, BookWriteSerializer,
    ReadingProgressSerializer, RegisterSerializer, UserSerializer,
)


# ── Auth ──────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    ser = RegisterSerializer(data=request.data)
    if ser.is_valid():
        user = ser.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data}, status=201)
    return Response(ser.errors, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    user = authenticate(username=request.data.get('username',''), password=request.data.get('password',''))
    if not user:
        return Response({'detail': 'Invalid credentials'}, status=401)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': UserSerializer(user).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'detail': 'Logged out'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


# ── Books ─────────────────────────────────────────────────────────────

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return BookWriteSerializer
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookListSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        qs   = Book.objects.all()
        q    = self.request.query_params.get('q', '')
        cat  = self.request.query_params.get('category', '')
        sort = self.request.query_params.get('sort', 'newest')
        if q:
            from django.db.models import Q
            qs = qs.filter(Q(title__icontains=q) | Q(author__icontains=q))
        if cat and cat != 'all':
            qs = qs.filter(category=cat)
        sort_map = {'newest': '-created_at', 'title': 'title', 'pages_asc': 'pages', 'pages_desc': '-pages'}
        return qs.order_by(sort_map.get(sort, '-created_at'))

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def seed(self, request):
        if Book.objects.exists():
            return Response({'detail': 'Books already exist. Wipe first.'}, status=400)
        demo = [
            ("The Orchard at Night","Marin Ellery",312,"Fiction","https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80","A translator takes a winter caretaker job in a coastal orchard."),
            ("Salt Roads","Ari Cho",286,"Fiction","https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=600&q=80","Three generations, one harbor town."),
            ("Paper Houses","Jules Renata",244,"Essays","https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80","Essays on living lightly."),
            ("Wintering Bees","T. K. Lark",198,"Poetry","https://images.unsplash.com/photo-1476275466078-4007374efbbe?auto=format&fit=crop&w=600&q=80","New poems for cold mornings."),
            ("The Mapmaker's Daughter","Sylvia Nwosu",401,"Fiction","https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=600&q=80","Charts, myths, and a missing archipelago."),
            ("Quiet Work","H. Moreau",176,"Nonfiction","https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=600&q=80","On focus in a noisy world."),
            ("Light Traps","R. V. Santos",328,"Art","https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=600&q=80","Photographic essays from the high desert."),
            ("The Slow Year","Beatrice Lin",265,"Essays","https://images.unsplash.com/photo-1491841573634-28140fc7ced7?auto=format&fit=crop&w=600&q=80","A calendar of noticing."),
            ("Stone & Salt","Jonas Firth",352,"Classics","https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80","A newly restored translation."),
            ("Narrow Rooms","P. N. Alvarez",210,"Fiction","https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=600&q=80","Seven linked stories."),
            ("Field Notes","M. Okonkwo",188,"Nonfiction","https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=600&q=80","Birdsong and bureaucracy."),
            ("Blue Hour","Elise Hart",224,"Poetry","https://images.unsplash.com/photo-1526243741027-444d633d7365?auto=format&fit=crop&w=600&q=80","Collected poems, 2018–2024."),
        ]
        Book.objects.bulk_create([Book(title=t,author=a,pages=p,category=c,cover_url=u,description=d) for t,a,p,c,u,d in demo])
        return Response({'seeded': len(demo)})

    @action(detail=False, methods=['delete'], permission_classes=[IsAdminUser])
    def wipe(self, request):
        count, _ = Book.objects.all().delete()
        return Response({'deleted': count})


# ── Reading progress ──────────────────────────────────────────────────

class ReadingProgressView(generics.ListCreateAPIView):
    serializer_class   = ReadingProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReadingProgress.objects.filter(user=self.request.user).select_related('book')

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        page    = request.data.get('page', 1)
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found'}, status=404)
        obj, _ = ReadingProgress.objects.update_or_create(
            user=request.user, book=book, defaults={'page': page}
        )
        ser = self.get_serializer(obj, context={'request': request})
        return Response(ser.data, status=200)
