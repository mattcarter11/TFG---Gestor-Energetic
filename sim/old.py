def _plot_bars(self, data, plot, showP, showL, stackL, showV, stackGSL, gaxis='both', lrot='vertical', xtimestamp = True):
        start = time()
        ax = plot.ax
        ax.clear()

        # List items to plot, it's color and legend labels
        bars = ['energyC', 'energyA', 'energyG']
        colors = [COLOR_EC, COLOR_EA, COLOR_EG]
        labels = ['Consumed', 'Available', 'Grid']
        # Show energy produced
        if showP:
            bars.insert(1, 'energyP')
            colors.insert(1, COLOR_EP)
            labels.insert(1, 'Produced')
        # Show energy loads separated
        barsL = ['energyLB', 'energyL1', 'energyL2']
        colorsL = [COLOR_LB, COLOR_L1, COLOR_L2]
        labelsL = ['Consumed Base Load', 'Consumed Load 1', 'Consumed Load 2']
        if showL and not stackL: 
            bars = barsL + bars
            colors = colorsL + colors
            labels = labelsL + labels
        # show unstacked energy available subtypes
        barsGSL = ['energyS', 'energyL', ]
        colorsGSL = [COLOR_ES, COLOR_EL, ]
        labelsGSL = ['Surplus', 'Lost', ]
        if not stackGSL:
            bars += barsGSL
            colors += colorsGSL
            labels += labelsGSL
        # Plot
        data.plot.bar(y=bars, ax=ax, color=colors, label=labels, width=0.60)
        # Add value labels
        if showV:
            for i, container in enumerate(ax.containers):
                label = [f'{p:.0f}' for p in data[bars[i]]]
                ax.bar_label(container, labels=label, rotation=lrot, color=colors[i], fontsize=10-int(0.4*len(bars)), padding=4)

        # stacked energy available subtypes
        if stackGSL: 
            pre_xlim = ax.get_xlim()
            width = ax.patches[0].get_width()
            pos = (len(bars)/2 - bars.index('energyA'))
            data.plot.bar(y=barsGSL, ax=ax, color=colorsGSL, label=labelsGSL, stacked=True, position=pos, width=width)
            # Add value labels
            if showV:
                for i, container in enumerate(ax.containers[-2:]):
                    label = [f'{p:.0f}' if p>0 else '' for p in data[barsGSL[i]]]
                    ax.bar_label(container, labels=label, rotation=lrot, fontsize=8-int(0.2*len(barsGSL)), color='#1e1e1e', label_type='center')
            ax.set_xlim(pre_xlim)      
        # stacked loads consumption 
        if showL and stackL: 
            pre_xlim = ax.get_xlim()
            width = ax.patches[0].get_width()
            pos = (len(bars)/2 - bars.index('energyC'))
            data.plot.bar(y=barsL, ax=ax, color=colorsL, label=labelsL, stacked=True, position=pos, width=width)
            # Add value labels
            if showV:
                for i, container in enumerate(ax.containers[-2:]):
                    label = [f'{p:.0f}' if p>0 else '' for p in data[barsL[i]]]
                    ax.bar_label(container, labels=label, rotation=lrot, fontsize=8-int(0.4*len(barsL)), color='#1e1e1e', label_type='center')
            ax.set_xlim(pre_xlim)
        
        # Visuals
        ax.margins(y=0.1)
        if xtimestamp:
            ax.set_xticklabels([x.strftime("%m-%d %H") for x in data['timestamp']], rotation=45)
            plot.fig.autofmt_xdate()
        else:
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.legend(loc="upper left")
        if gaxis != None:
            ax.grid(True, linestyle=':', axis=gaxis)
        ax.set_xlabel('Date & Time')
        ax.set_ylabel('Energy [Wh]')
        ax.set_title('Energy Balance')
        # Draw
        plot.draw()
        self.ui.plotting_time.setText(f'Plotting Time: {time()-start:.3f} s')