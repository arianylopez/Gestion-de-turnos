
from cola import Cola
from lista import Lista

class TicketSystem:
    def __init__(self):
        self.priority_cola = Cola()
        self.general_cola = Cola()
        self.currency_exchange_cola = Cola()
        self.general_counter = 0
        self.priority_counter = 0
        self.general_ticket_counter = 0
        self.currency_counter = 0
        self.ordered_tickets = Lista()

    def insertar_general(self):
        self.general_ticket_counter += 1
        ticket_id = f"G-{self.general_ticket_counter}"
        self.general_cola.encolar("General", ticket_id)
        self.ordered_tickets.agregar((ticket_id, "General"))
        return ticket_id

    def insertar_preferencial(self):
        self.priority_counter += 1
        ticket_id = f"P-{self.priority_counter}"
        self.priority_cola.encolar("Preferencial", ticket_id)
        self.ordered_tickets.agregar((ticket_id, "Preferencial"))
        return ticket_id

    def insertar_cambio_de_moneda(self):
        self.currency_counter += 1
        ticket_id = f"C-{self.currency_counter}"
        self.currency_exchange_cola.encolar("Cambio de Moneda", ticket_id)
        self.ordered_tickets.agregar((ticket_id, "Cambio de Moneda"))
        return ticket_id

    def next_ticket(self):
        ticket = None
        if self.priority_cola.head is not None:
            ticket = self.priority_cola.desencolar()
        elif self.general_counter >= 2 and self.currency_exchange_cola.head is not None:
            self.general_counter = 0
            ticket = self.currency_exchange_cola.desencolar()
        elif self.general_cola.head is not None:
            self.general_counter += 1
            ticket = self.general_cola.desencolar()
        elif self.currency_exchange_cola.head is not None:
            ticket = self.currency_exchange_cola.desencolar()
        
        if ticket:
            self.ordered_tickets.eliminar(ticket.value)
        
        return ticket

    def cancel_ticket(self, ticket_to_cancel):
        cancelled = False
        if self.priority_cola.remove_ticket(ticket_to_cancel):
            cancelled = True
        elif self.general_cola.remove_ticket(ticket_to_cancel):
            cancelled = True
        elif self.currency_exchange_cola.remove_ticket(ticket_to_cancel):
            cancelled = True
        
        if cancelled:
            self.ordered_tickets.eliminar(ticket_to_cancel)
        
        return cancelled

    def show_status(self):
        tickets = self.ordered_tickets.mostrar()
        result = []
        for ticket in tickets:
            formatted_ticket = f"{ticket[0]}"
            result.append(formatted_ticket)
        return result

# Pruebas 
ticket = TicketSystem()
ticket.insertar_general()
ticket.insertar_preferencial()
ticket.insertar_cambio_de_moneda()
ticket.insertar_general()
ticket.insertar_general()
ticket.insertar_preferencial()

print(ticket.show_status())
ticket.next_ticket()
print(ticket.show_status())
ticket.cancel_ticket("P-2")
print(ticket.show_status())
