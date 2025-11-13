import tkinter as tk
from tkinter import ttk, messagebox

class PDVApp:
    def __init__(self, root):
        self.root = root
        root.title('PDV - Autoatendimento')
        root.geometry('1000x600')

        self.create_widgets()

    def create_widgets(self):
        # Topo
        top = ttk.Frame(self.root)
        top.pack(fill='x', padx=8, pady=6)

        title = ttk.Label(top, text='Sistema de Autoatendimento - PDV', font=('Arial', 16, 'bold'))
        title.pack(side='left')

        admin_btn = ttk.Button(top, text='Login Admin', command=self.open_admin_login)
        admin_btn.pack(side='right')

        # Corpo Principal
        main = ttk.Frame(self.root)
        main.pack(fill='both', expand=True, padx=8, pady=6)

        # Área de produtos
        left = ttk.Frame(main)
        left.pack(side='left', fill='both', expand=True)

        left_label = ttk.Label(left, text='Produtos Disponíveis', font=('Arial', 12, 'bold'))
        left_label.pack(anchor='w', pady=4)

        # Lista de produtos
        products_canvas = tk.Canvas(left)
        products_frame = ttk.Frame(products_canvas)
        vsb = ttk.Scrollbar(left, orient='vertical', command=products_canvas.yview)
        products_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        products_canvas.pack(fill='both', expand=True)
        products_canvas.create_window((0, 0), window=products_frame, anchor='nw')

        # Produtos de exemplo
        for i in range(6):
            frame = ttk.Frame(products_frame, relief='raised', padding=6)
            frame.grid(row=i // 3, column=i % 3, padx=6, pady=6, sticky='nsew')
            ttk.Label(frame, text=f'Produto {i + 1}', font=('Arial', 11)).pack(anchor='w')
            ttk.Label(frame, text='R$ 0,00', font=('Arial', 10, 'italic')).pack(anchor='w')
            ttk.Button(frame, text='Adicionar').pack(pady=4, fill='x')

        # Área do carrinho
        right = ttk.Frame(main, width=320)
        right.pack(side='right', fill='y')

        cart_label = ttk.Label(right, text='Carrinho', font=('Arial', 12, 'bold'))
        cart_label.pack(anchor='w', pady=4)

        self.cart_listbox = tk.Listbox(right, height=20)
        self.cart_listbox.pack(fill='both', expand=True, padx=2)

        # Botões do carrinho
        cart_controls = ttk.Frame(right)
        cart_controls.pack(fill='x')
        ttk.Button(cart_controls, text='Remover item').pack(side='left', padx=4, pady=6)
        ttk.Button(cart_controls, text='Limpar carrinho').pack(side='left', padx=4, pady=6)

        self.total_label = ttk.Label(right, text='Total: R$ 0,00', font=('Arial', 12, 'bold'))
        self.total_label.pack(anchor='e', padx=8)

        ttk.Button(right, text='Checkout (PIX)', command=self.checkout).pack(fill='x', padx=8, pady=6)

    # Tela de Login do Administrador
    def open_admin_login(self):
        login_win = tk.Toplevel(self.root)
        login_win.title('Login do Administrador')
        login_win.geometry('300x200')

        ttk.Label(login_win, text='Usuário:').pack(pady=4)
        user_entry = ttk.Entry(login_win)
        user_entry.pack(pady=4)

        ttk.Label(login_win, text='Senha:').pack(pady=4)
        pass_entry = ttk.Entry(login_win, show='*')
        pass_entry.pack(pady=4)

        ttk.Button(login_win, text='Entrar', command=lambda: self.validate_admin(user_entry.get(), pass_entry.get(), login_win)).pack(pady=10)

    def validate_admin(self, user, password, window):
        if user == "admin" and password == "123":
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            window.destroy()
            self.open_admin_panel()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    # Painel do Administrador
    def open_admin_panel(self):
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Painel do Administrador")
        admin_win.geometry("400x300")

        ttk.Label(admin_win, text="Gerenciamento de Produtos", font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Button(admin_win, text="Adicionar Produto").pack(pady=6)
        ttk.Button(admin_win, text="Editar Produto").pack(pady=6)
        ttk.Button(admin_win, text="Excluir Produto").pack(pady=6)

    # Checkout
    def checkout(self):
        checkout_win = tk.Toplevel(self.root)
        checkout_win.title("Checkout - Pagamento PIX")
        checkout_win.geometry("300x300")

        ttk.Label(checkout_win, text="Valor total: R$ 0,00", font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Label(checkout_win, text="Escaneie o QR Code para pagar").pack(pady=10)
        ttk.Label(checkout_win, text="[QR CODE PIX]").pack(pady=20)
        ttk.Button(checkout_win, text="Confirmar Pagamento").pack(pady=10)

# Execução principal
if __name__ == '__main__':
    root = tk.Tk()
    app = PDVApp(root)
    root.mainloop()
