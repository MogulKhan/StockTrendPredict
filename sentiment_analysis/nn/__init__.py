import torch

x = torch.empty(5, 3)
print(type(x))

x = torch.rand([5, 3])
print(x)
print(type(x))

print(x[:, 1])
print(x[1, :])

x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8) # the size -1 is inferred from other dimensions
print(x.size(), y.size(), z.size())

x = torch.randn(1)
print(x)
print(x.item())

x = torch.randn(3, requires_grad=True)
print(x)

y = x * 2
print(y.data.norm())