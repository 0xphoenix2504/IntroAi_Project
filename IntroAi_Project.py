# tkinter Library for GUI
import tkinter as tk 
from tkinter import ttk

import math 

#--------------Price Negotiation Strategy Engine----------------

# --------------Main Core Functions----------------

minimax_nodes    = 0
Alpha_Beta_nodes = 0


def Evaluate(seller_price , buyer_offer) :
    """
    - This Function Compares the Buyer's Offer and the Seller's Price
    - If the Seller's Price is good for the Buyer , He will get a High Score
    - If the Buyer walks away ,it will Return a low Score
    """

    if buyer_offer >= seller_price :  
        return 1000 + seller_price   # The 1000 Guarantee a High Score if the Seller wins
    
    if buyer_offer < 0 :
        return -999999
    
    
         
    return -(seller_price - buyer_offer)  

def minimax (seller_price , buyer_offer , depth , is_seller_turn) :
    global minimax_nodes  # Global Variable to Count the Number of Nodes in the Minimax Tree
    minimax_nodes += 1


    Seller_Move = [-5 , 0 , 3]
    Buyer_Move = [5 , 0 , "WALK AWAY"]


    if depth == 0 : # Stop when the tree is over
        return Evaluate(seller_price , buyer_offer)
    
    if buyer_offer >= seller_price : # Stop If there is a deal
        return Evaluate(seller_price , buyer_offer) 
    

    if is_seller_turn :
        best =  -math.inf    # Assign the best value to -infinity
         

        for move in Seller_Move :    # Reassign the seller price in the negotiation
            new_seller_price = seller_price + move 
            value = minimax(new_seller_price , buyer_offer , depth-1 , False) 
            best = max(best , value)
        return best
    

    else:
        best = math.inf   # Assign the best value to infinity


        for move in Buyer_Move :
            if move == "WALK AWAY" :
                best = min (best , -999999)
                continue

            new_buyer_offer = buyer_offer + move 
            value = minimax(seller_price , new_buyer_offer , depth -1 , True)
            best = min (best , value)
        return best        



def Alpha_Beta(Seller_price , buyer_offer ,depth , alpha , beta , is_seller_turn):
    global Alpha_Beta_nodes  # Global Variable to Count the Number of Nodes in the Alpha-Beta Tree
    Alpha_Beta_nodes += 1


    Seller_Move = [-5 , 0 , 3]
    Buyer_Move = [5 , 0 , "WALK AWAY"]

    if depth == 0 : # Stop when the tree is over
        return Evaluate(Seller_price , buyer_offer)
    
    if buyer_offer >= Seller_price : # Stop If there is a deal
        return Evaluate(Seller_price , buyer_offer)
    
    if is_seller_turn :
        best =  -math.inf    # Assign the best value to -infinity
         

        for move in Seller_Move :    # Reassign the seller price in the negotiation
            new_seller_price = Seller_price + move 
            value = Alpha_Beta(new_seller_price , buyer_offer , depth-1 , alpha , beta , False) 
            best = max(best , value)
            alpha = max(alpha , best)

            if beta <= alpha :  # Beta Cutting
                break

        return best
    
    else:
        best = math.inf   # Assign the best value to infinity


        for move in Buyer_Move :
            if move == "WALK AWAY" :
                best = min (best , -999999)
                beta = min(beta , best)
                if beta <= alpha :  # Alpha Cutting
                    break   
                continue

            new_buyer_offer = buyer_offer + move
            value = Alpha_Beta(Seller_price , new_buyer_offer , depth -1 , alpha , beta , True)
            best = min (best , value)
            beta = min(beta , best)

            if beta <= alpha :  # Alpha Cutting
                break

        return best        
    
def get_optimal_path (seller_price , buyer_offer):
    """
        - This Function Returns the Optimal Path of the Negotiation between the Seller and the Buyer
        - It Uses the Alpha-Beta Pruning Algorithm to Get the Optimal Solution for Each Player
    """

    Buyer_Move = [5 , 0 , "WALK AWAY"]

    optimal_path = []
    alpha = -math.inf
    beta = math.inf

    for round_num in range (1,11) :  # We will have 10 Rounds of Negotiation

        if buyer_offer >= seller_price :
            break   

        Seller_Move = [-5 , 0 , 3]
        best_value = -math.inf
        best_move = 0

        for move in Seller_Move :
            new_seller_price = seller_price + move 
            value = Alpha_Beta(new_seller_price , buyer_offer , 6 , alpha , beta , False)  # The depth is 6 For 3 Rounds for Each Player 

            if value > best_value :
                best_value = value
                best_move = move


        seller_price += best_move
        alpha = max(alpha , best_value)

        if best_move == 0 :
            action = "Hold"

        elif best_move > 0 :
            action = f"Increase Price by {best_move}"

        else :
            action = f"Decrease Price by {best_move}"

        optimal_path.append( # Append the Current State of the Negotiation to the Optimal Path
        {  "Round" : round_num ,"Agent" : "Seller" , "Action" : action , "Seller Price" : seller_price ,
           "Buyer Offer" : buyer_offer , "Alpha" : alpha , "Beta" : beta
        } )   

        if buyer_offer >= seller_price :
            break

        best_value  = math.inf 
        best_move = 0

        for move in Buyer_Move :
            if move == "WALK AWAY" :
                value = -999999
            else :
                new_buyer_offer = buyer_offer + move
                value = Alpha_Beta(seller_price , new_buyer_offer , 6-round_num , alpha , beta , True)

            if value < best_value :
                  best_value = value
                  best_move  = move
       
        beta = min(beta , best_value)

        if best_move == "WALK AWAY" :
            optimal_path.append( # Append the Current State of the Negotiation to the Optimal Path
                { "Round" : round_num ,"Agent" : "Buyer" , "Action" : "WALK AWAY" , "Seller Price" : seller_price ,
                  "Buyer Offer" : buyer_offer , "Alpha" : alpha , "Beta" : beta })
            return optimal_path , "The Buyer Walked Away !!" , None

        buyer_offer += best_move  

        action = "Hold" if best_move == 0 else f"Increase Offer by {best_move}"

        optimal_path.append(# Append the Current State of the Negotiation to the Optimal Path
            { "Round" : round_num , "Agent" : "Buyer" , "Action" : action , "Seller Price" : seller_price ,
              "Buyer Offer" : buyer_offer , "Alpha" : alpha , "Beta" : beta })

    if buyer_offer >= seller_price :
        return optimal_path , "We Had A Deal !!" , seller_price
        
    return optimal_path , f"No Deal After {round_num - 1} Rounds" , None



def compare_nodes (seller_price , buyer_offer ) : # This Function Compares Between Minimax and Alpha-Beta
    global minimax_nodes
    global Alpha_Beta_nodes

    minimax_nodes = 0
    Alpha_Beta_nodes = 0

    minimax(seller_price , buyer_offer , 6 , True)
    Alpha_Beta(seller_price , buyer_offer , 6 , -math.inf , math.inf , True)

    pruning_percentage = round ((1 - Alpha_Beta_nodes / minimax_nodes) * 100 ,2 )

    return  {
        "Minimax Nodes" : minimax_nodes ,
        "Alpha-Beta Nodes" : Alpha_Beta_nodes ,
        "Pruning Percentage" : f"{pruning_percentage} %"
    }




#------------------GUI------------------

# ─── Main Window ───
root = tk.Tk()
root.title("Price Negotiation Strategy Engine")
root.geometry("900x700")
root.configure(bg="#1e1e2e")

# ─── Title ───
title_label = tk.Label(
    root,
    text="Price Negotiation Strategy Engine",
    font=("Arial", 18, "bold"),
    bg="#1e1e2e",
    fg="#cdd6f4"
)
title_label.pack(pady=20)

# ─── Input Frame ───
input_frame = tk.Frame(root, bg="#313244", padx=20, pady=20)
input_frame.pack(fill="x", padx=30, pady=10)

# Seller Price
seller_label = tk.Label(
    input_frame,
    text="Seller Starting Price :",
    font=("Arial", 12),
    bg="#313244",
    fg="#cdd6f4"
)
seller_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

seller_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=10,
    bg="#45475a",
    fg="#cdd6f4",
    insertbackground="#cdd6f4"
)
seller_entry.insert(0, "100")
seller_entry.grid(row=0, column=1, padx=10, pady=10)

# Buyer Budget
buyer_label = tk.Label(
    input_frame,
    text="Buyer Starting Budget :",
    font=("Arial", 12),
    bg="#313244",
    fg="#cdd6f4"
)
buyer_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

buyer_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=10,
    bg="#45475a",
    fg="#cdd6f4",
    insertbackground="#cdd6f4"
)
buyer_entry.insert(0, "70")
buyer_entry.grid(row=0, column=3, padx=10, pady=10)

# Run Button
run_button = tk.Button(
    input_frame,
    text="Run Negotiation",
    font=("Arial", 12, "bold"),
    bg="#89b4fa",
    fg="#1e1e2e",
    padx=15,
    pady=5,
    cursor="hand2",
    command=lambda: run_negotiation()
)
run_button.grid(row=0, column=4, padx=20, pady=10)


# ─── Notebook (Tabs) ───
notebook = ttk.Notebook(root)
notebook.pack(fill="x", expand=False, padx=30, pady=10)  # ← expand=False و fill="x"

# Tab 1 — Results Table
tab1 = tk.Frame(notebook, bg="#313244", height=200)  # ← height ثابت
notebook.add(tab1, text="  Negotiation Results  ")

results_label = tk.Label(
    tab1,
    text="Negotiation Results",
    font=("Arial", 13, "bold"),
    bg="#313244",
    fg="#cdd6f4"
)
results_label.pack(anchor="w", pady=5, padx=10)

columns = ("Round", "Agent", "Action", "Seller Price", "Buyer Offer", "Alpha", "Beta")
tree = ttk.Treeview(tab1, columns=columns, show="headings", height=6)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)
tree.pack(fill="both", expand=True, padx=10, pady=5)

# Tab 2 — Negotiation Tree
tab2 = tk.Frame(notebook, bg="#1e1e2e", height=200)
notebook.add(tab2, text="  Negotiation Tree  ")

# ─── Scrollbars ───
scroll_y = tk.Scrollbar(tab2, orient="vertical")
scroll_x = tk.Scrollbar(tab2, orient="horizontal")
scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")

tree_canvas = tk.Canvas(
    tab2,
    bg="#1e1e2e",
    highlightthickness=0,
    height=200,
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)
tree_canvas.pack(fill="both", expand=True)

scroll_y.config(command=tree_canvas.yview)
scroll_x.config(command=tree_canvas.xview)

# ─── Outcome Label ───
outcome_label = tk.Label(
    root,
    text="",
    font=("Arial", 13, "bold"),
    bg="#1e1e2e",
    fg="#a6e3a1"
)
outcome_label.pack(pady=8)    

# ─── Stats Frame ───
stats_frame = tk.Frame(root, bg="#313244", padx=20, pady=15)
stats_frame.pack(fill="x", padx=30, pady=10)

minimax_label   = tk.Label(stats_frame, text="Minimax Nodes  : ", font=("Arial", 11), bg="#313244", fg="#cdd6f4")
alphabeta_label = tk.Label(stats_frame, text="Alpha-Beta Nodes : ", font=("Arial", 11), bg="#313244", fg="#cdd6f4")
pruning_label   = tk.Label(stats_frame, text="Pruning %  : ", font=("Arial", 11), bg="#313244", fg="#cdd6f4")

minimax_label.grid  (row=0, column=0, padx=20, pady=5)
alphabeta_label.grid(row=0, column=1, padx=20, pady=5)
pruning_label.grid  (row=0, column=2, padx=20, pady=5)


def format_val(v):
    if v >= 1000:       return "Deal"
    if v == -999999:    return "-inf"
    if v == math.inf:   return "+inf"
    if v == -math.inf:  return "-inf"
    return round(v, 2)   

def draw_tree(seller_price, buyer_offer):
    tree_canvas.delete("all")
    tree_canvas.config(scrollregion=(0, 0, 1200, 600))  # ← كبّر المساحة

    Seller_Move = [-5, 0, 3]
    Buyer_Move  = [5, 0, "WALK AWAY"]

    W      = 900
    node_r = 32

    def draw_node(x, y, text1, text2, color, pruned=False):
        fill    = "#555566" if pruned else color
        outline = "#888899" if pruned else "#ffffff"
        tc      = "#888899" if pruned else "#ffffff"
        tree_canvas.create_oval(x-node_r, y-node_r, x+node_r, y+node_r,
                                fill=fill, outline=outline, width=1.5)
        tree_canvas.create_text(x, y-9, text=text1, fill=tc,
                                font=("Arial", 9, "bold"))
        tree_canvas.create_text(x, y+9, text=text2, fill=tc,
                                font=("Arial", 8))

    def draw_edge(x1, y1, x2, y2, label, pruned=False):
        color = "#555566" if pruned else "#89b4fa"
        dash  = (5, 4)   if pruned else ()
        tree_canvas.create_line(x1, y1+node_r, x2, y2-node_r,
                                fill=color, width=1.5, dash=dash)
        mx = (x1+x2)/2
        my = (y1+y2)/2 - 10
        tree_canvas.create_text(mx, my, text=label,
                                fill="#a6adc8" if not pruned else "#555566",
                                font=("Arial", 8))

    # ─── Level 0: Root ───
    rx, ry = W//2, 60
    draw_node(rx, ry, f"S:{seller_price}", f"B:{buyer_offer}", "#89b4fa")

    # ─── Level 1: Seller moves ───
    l1_xs  = [rx-310, rx, rx+310]
    l1_y   = 200
    s_lbls = ["-5", "Hold", "+3"]
    alpha  = -math.inf

    for i, (sm, lx) in enumerate(zip(Seller_Move, l1_xs)):
        nsp   = seller_price + sm
        score = Alpha_Beta(nsp, buyer_offer, 4, -math.inf, math.inf, False)

        draw_edge(rx, ry, lx, l1_y, s_lbls[i])
        s_txt = f"{round(score,0)}" if score > -999990 else "WA"
        draw_node(lx, l1_y, f"S:{nsp}", s_txt, "#cba6f7")

        alpha = max(alpha, score)

        # ─── Level 2: Buyer moves ───
        l2_xs  = [lx-95, lx, lx+95]
        l2_y   = 370
        b_lbls = ["+5", "Hold", "WA"]
        beta   = math.inf
        pruned_b = False

        for j, (bm, bx) in enumerate(zip(Buyer_Move, l2_xs)):
            if bm == "WALK AWAY":
                bs    = -999999
                btxt1 = "WALK"
                btxt2 = "AWAY"
            else:
                nbo   = buyer_offer + bm
                bs    = Alpha_Beta(nsp, nbo, 3, -math.inf, math.inf, True)
                btxt1 = f"B:{nbo}"
                btxt2 = f"{round(bs,0)}" if bs > -999990 else "WA"

            draw_edge(lx, l1_y, bx, l2_y, b_lbls[j], pruned_b)
            draw_node(bx, l2_y, btxt1, btxt2, "#a6e3a1", pruned_b)

            if not pruned_b:
                beta = min(beta, bs)
                if beta <= alpha:
                    pruned_b = True

    # ─── Legend ───
    legend_items = [
        (30, 30, "#89b4fa", "Seller (MAX)"),
        (30, 75, "#cba6f7", "Buyer (MIN)"),
        (30, 120, "#a6e3a1", "Buyer leaf"),
        (30, 165, "#555566", "Pruned"),
    ]
    for lx, ly, lc, lt in legend_items:
        tree_canvas.create_oval(lx, ly, lx+22, ly+22, fill=lc, outline="")
        tree_canvas.create_text(lx+32, ly+11, text=lt,
                                fill="#cdd6f4", font=("Arial", 9), anchor="w")
notebook.pack(fill="x", expand=False, padx=30, pady=10)

# ─── Run Negotiation Function ───
def run_negotiation():
    try:
        seller_price = int(seller_entry.get())
        buyer_offer  = int(buyer_entry.get())
    except ValueError:
        outcome_label.config(text="Please enter valid numbers!", fg="#f38ba8")
        return


    # امسح الجدول القديم
    for row in tree.get_children():
        tree.delete(row)

    # شغّل الـ logic
    path, outcome, final_price = get_optimal_path(seller_price, buyer_offer)
    stats = compare_nodes(seller_price, buyer_offer)

    # املا الجدول
    for step in path:
      tree.insert("", "end", values=(
         step["Round"],
         step.get("Agent", "—"),
         step["Action"],
         step["Seller Price"],
         step["Buyer Offer"],
         format_val(step["Alpha"]),
         format_val(step["Beta"])
    ))
     
    # اعرض النتيجة
    if outcome == "We Had A Deal !!":
        outcome_label.config(
            text=f"Deal at Price: {final_price}",
            fg="#a6e3a1"
        )
    else:
        outcome_label.config(
            text=outcome,
            fg="#f38ba8"
        )

   # ارسم الشجرة
    draw_tree(seller_price, buyer_offer)

    # اعرض الـ stats
    minimax_label.config  (text=f"Minimax Nodes   : {stats['Minimax Nodes']}")
    alphabeta_label.config(text=f"Alpha-Beta Nodes : {stats['Alpha-Beta Nodes']}")
    pruning_label.config  (text=f"Pruning %        : {stats['Pruning Percentage']}")



root.mainloop()







