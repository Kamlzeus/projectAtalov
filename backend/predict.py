import torch
from torchvision import transforms
from torchvision.models import resnet50
from torchvision.models import ResNet50_Weights
from PIL import Image

# Используем GPU, если доступен
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Загружаем предобученную ResNet50 и подставляем классификатор на 10 классов
model = resnet50(weights=ResNet50_Weights.DEFAULT)
model.fc = torch.nn.Linear(model.fc.in_features, 10)
model.load_state_dict(torch.load('resnet50_paintingsss.pth', map_location=device))
model.eval()
model.to(device)

# Новые классы (10 стилей живописи)
class_names = [
    'Baroque', 'Cubism', 'Expressionism', 'Impressionism', 'Minimalism',
    'Pop_Art', 'Post_Impressionism', 'Realism', 'Rococo', 'Romanticism'
]

# Трансформация изображения
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Предсказание
def predict_image(file):
    image = Image.open(file).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)

    return class_names[predicted.item()]
