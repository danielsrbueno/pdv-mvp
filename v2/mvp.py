import tkinter as tk
from tkinter import ttk, messagebox

class PDVApp:
    def __init__(self, root):
        self.root = root
        root.title('PDV - Autoatendimento')
        root.geometry('1000x600')

        self.products = [
            {'nome': 'Refrigerante', 'preco': 5.00},
            {'nome': 'Batata Frita', 'preco': 12.00},
            {'nome': 'Hambúrguer', 'preco': 18.00},
            {'nome': 'Pizza', 'preco': 25.00},
            {'nome': 'Suco Natural', 'preco': 8.00},
            {'nome': 'Pudim', 'preco': 7.00},
        ]

        self.cart = []
        self.create_widgets()

    # INTERFACE
    def create_widgets(self):
        top = ttk.Frame(self.root)
        top.pack(fill='x', padx=8, pady=6)

        ttk.Label(top, text='Sistema de Autoatendimento - PDV', font=('Arial', 16, 'bold')).pack(side='left')
        ttk.Button(top, text='Login Admin', command=self.open_admin_login).pack(side='right')

        main = ttk.Frame(self.root)
        main.pack(fill='both', expand=True, padx=8, pady=6)

        # Produtos
        left = ttk.Frame(main)
        left.pack(side='left', fill='both', expand=True)

        ttk.Label(left, text='Produtos Disponíveis', font=('Arial', 12, 'bold')).pack(anchor='w', pady=4)

        self.products_canvas = tk.Canvas(left)
        self.products_frame = ttk.Frame(self.products_canvas)
        vsb = ttk.Scrollbar(left, orient='vertical', command=self.products_canvas.yview)
        self.products_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self.products_canvas.pack(fill='both', expand=True)
        self.products_canvas.create_window((0, 0), window=self.products_frame, anchor='nw')

        self.products_frame.bind("<Configure>", lambda e: self.products_canvas.configure(scrollregion=self.products_canvas.bbox("all")))

        self.render_products()

        # Carrinho
        right = ttk.Frame(main, width=320)
        right.pack(side='right', fill='y')

        ttk.Label(right, text='Carrinho', font=('Arial', 12, 'bold')).pack(anchor='w', pady=4)
        self.cart_listbox = tk.Listbox(right, height=20)
        self.cart_listbox.pack(fill='both', expand=True, padx=2)

        controls = ttk.Frame(right)
        controls.pack(fill='x')
        ttk.Button(controls, text='Remover item', command=self.remove_from_cart).pack(side='left', padx=4, pady=6)
        ttk.Button(controls, text='Limpar carrinho', command=self.clear_cart).pack(side='left', padx=4, pady=6)

        self.total_label = ttk.Label(right, text='Total: R$ 0,00', font=('Arial', 12, 'bold'))
        self.total_label.pack(anchor='e', padx=8)
        ttk.Button(right, text='Checkout (PIX)', command=self.checkout).pack(fill='x', padx=8, pady=6)

    # Funções de Produtos
    def render_products(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        for i, p in enumerate(self.products):
            frame = ttk.Frame(self.products_frame, relief='raised', padding=6)
            frame.grid(row=i // 3, column=i % 3, padx=6, pady=6, sticky='nsew')
            ttk.Label(frame, text=p['nome'], font=('Arial', 11, 'bold')).pack(anchor='w')
            ttk.Label(frame, text=f"R$ {p['preco']:.2f}", font=('Arial', 10, 'italic')).pack(anchor='w')
            ttk.Button(frame, text='Adicionar', command=lambda prod=p: self.add_to_cart(prod)).pack(pady=4, fill='x')

    def add_to_cart(self, product):
        self.cart.append(product)
        self.update_cart_display()

    def remove_from_cart(self):
        selection = self.cart_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para remover.")
            return
        index = selection[0]
        self.cart.pop(index)
        self.update_cart_display()

    def clear_cart(self):
        if not self.cart:
            messagebox.showinfo("Carrinho", "O carrinho já está vazio.")
            return
        if messagebox.askyesno("Limpar carrinho", "Deseja remover todos os itens?"):
            self.cart.clear()
            self.update_cart_display()

    def update_cart_display(self):
        self.cart_listbox.delete(0, tk.END)
        total = 0
        for item in self.cart:
            self.cart_listbox.insert(tk.END, f"{item['nome']} - R$ {item['preco']:.2f}")
            total += item['preco']
        self.total_label.config(text=f"Total: R$ {total:.2f}")

    # Login Admin
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

        ttk.Button(
            login_win,
            text='Entrar',
            command=lambda: self.validate_admin(user_entry.get(), pass_entry.get(), login_win)
        ).pack(pady=10)

    def validate_admin(self, user, password, window):
        if user == "admin" and password == "123":
            window.destroy()
            self.open_admin_panel()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    # Painel do Administrador
    def open_admin_panel(self):
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Painel do Administrador")
        admin_win.geometry("400x400")

        ttk.Label(admin_win, text="Gerenciamento de Produtos", font=('Arial', 12, 'bold')).pack(pady=10)

        form = ttk.Frame(admin_win)
        form.pack(pady=10)

        ttk.Label(form, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        nome_entry = ttk.Entry(form)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Preço:").grid(row=1, column=0, padx=5, pady=5)
        preco_entry = ttk.Entry(form)
        preco_entry.grid(row=1, column=1, padx=5, pady=5)

        def add_product():
            nome = nome_entry.get()
            preco = preco_entry.get()
            if not nome or not preco:
                messagebox.showwarning("Erro", "Preencha todos os campos.")
                return
            try:
                preco = float(preco)
            except ValueError:
                messagebox.showwarning("Erro", "Preço inválido.")
                return
            self.products.append({'nome': nome, 'preco': preco})
            self.render_products()
            nome_entry.delete(0, tk.END)
            preco_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Produto adicionado!")

        ttk.Button(form, text="Adicionar Produto", command=add_product).grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Separator(admin_win).pack(fill='x', pady=8)

        ttk.Label(admin_win, text="Produtos atuais:").pack()
        listbox = tk.Listbox(admin_win)
        listbox.pack(fill='both', expand=True, padx=8, pady=4)
        for p in self.products:
            listbox.insert(tk.END, f"{p['nome']} - R$ {p['preco']:.2f}")

        def delete_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("Erro", "Selecione um produto para excluir.")
                return
            index = sel[0]
            del self.products[index]
            listbox.delete(index)
            self.render_products()
            messagebox.showinfo("Removido", "Produto excluído com sucesso.")

        ttk.Button(admin_win, text="Excluir Produto", command=delete_selected).pack(pady=5)

    # Checkout
    def checkout(self):
        total = sum(p['preco'] for p in self.cart)
        checkout_win = tk.Toplevel(self.root)
        checkout_win.title("Checkout - Pagamento PIX")
        checkout_win.geometry("300x300")

        ttk.Label(checkout_win, text=f"Valor total: R$ {total:.2f}", font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Label(checkout_win, text="Escaneie o QR Code para pagar").pack(pady=10)
        ttk.Label(checkout_win, text="[QR CODE PIX]").pack(pady=20)
        ttk.Button(checkout_win, text="Confirmar Pagamento", command=lambda: self.finish_checkout(checkout_win)).pack(pady=10)

    def finish_checkout(self, window):
        messagebox.showinfo("Pagamento", "Pagamento confirmado com sucesso!")
        window.destroy()
        self.clear_cart()

# Execução principal
if __name__ == '__main__':
    root = tk.Tk()
    app = PDVApp(root)
    root.mainloop()
